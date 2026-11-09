from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton, QSizePolicy, QCheckBox, QLineEdit

from core.utils import get_window_dimension as g
from core.config import PLATFORM, VERSION
from ui.hidden_wnd import RSAPHiddenWnd
from ui.settings_wnd import SettingsWnd
from ui.about_wnd import RSAPAboutWnd
from core.rand_engine import RandomEngine
from core.settings import load as l
from core.translator import tr

import logging

lgr = logging.getLogger(__name__)

class RSAPMainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		lgr.info('Main window initiated')
		if PLATFORM == 'Linux':
			lgr.warning('Running on Linux. Some window features, such as stay on top, may not function correctly')

		if int(l('stay_on_top', 1)):
			self.on_top = 1
			self.setWindowFlags(Qt.WindowStaysOnTopHint)
		else:
			self.on_top = 0

		self.hiddenwnd = RSAPHiddenWnd(self)
		self.settings_wnd = SettingsWnd(self)
		self.aboutwnd = RSAPAboutWnd(self)

		self.setWindowTitle('RSAP')

		if not int(l('wnd_behavior', 0)):
			try:
				self.setFixedSize(l('initsz', g()))
			except:
				self.setFixedSize(int(l('initsz', g())[0]), int(l('initsz', g())[1]))
		else:
			try:
				self.resize(l('initsz', g()))
			except:
				self.resize(int(l('initsz', g())[0]), int(l('initsz', g())[1]))
		lgr.info('Window parameters set')

		self.setup_ui()
		lgr.info('Main UI is now set up')

		self.random_engine = RandomEngine(self)

		self.connect_signals()
		lgr.info('Signals are now connected')
		self.resize_widgets()

	def setup_ui(self):
		self.main_layout = QHBoxLayout()
		self.main_widget = QWidget()
		self.main_widget.setLayout(self.main_layout)

		self.nn_layout = QVBoxLayout()
		self.nn_widget = QWidget()
		self.nn_widget.setLayout(self.nn_layout)

		self.number_label = QLineEdit()
		self.number_label.setText('??')
		self.number_label.setReadOnly(True)
		self.number_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
		self.number_label.setFont(QFont('Consolas', self.height() // 2))
		self.number_label.setStyleSheet('color: #0094FF; font-weight: bold; background: transparent; border: none;')
		self.nn_layout.addWidget(self.number_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

		self.name_label = QLineEdit()
		self.name_label.setText('')
		self.name_label.setReadOnly(True)
		self.name_label.setStyleSheet('background: transparent; border: none;')
		self.name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
		tmp_font = self.name_label.font()
		tmp_font.setPointSize(self.height() // 6)
		self.name_label.setFont(tmp_font)
		self.nn_layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
		
		self.number_label.home(False)
		self.name_label.home(False)

		self.nn_layout.setSpacing(0)
		self.main_layout.addWidget(self.nn_widget, alignment=Qt.AlignmentFlag.AlignHCenter, stretch=1)

		self.sep1 = QFrame()
		self.sep1.setFrameShape(QFrame.VLine)
		self.main_layout.addWidget(self.sep1, alignment=Qt.AlignmentFlag.AlignLeft)

		self.tools_layout = QVBoxLayout()
		self.tools_widget = QWidget()
		self.tools_widget.setLayout(self.tools_layout)

		self.step_btn = QPushButton(tr('mainwnd_step'), self)
		self.step_btn.setFixedWidth(self.width() * 2 // 5)
		self.step_btn.setFixedHeight(self.height() // 3)
		tmp_font = self.step_btn.font()
		tmp_font.setPointSize(self.height() // 20)
		self.step_btn.setFont(tmp_font)
		self.tools_layout.addWidget(self.step_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.start_btn = QPushButton(tr('mainwnd_start'), self)
		self.start_btn.setFixedWidth(self.width() * 2 // 5)
		self.start_btn.setFixedHeight(self.height() // 3)
		self.start_btn.setFont(tmp_font)
		self.tools_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.sep2 = QFrame()
		self.sep2.setFrameShape(QFrame.HLine)
		self.tools_layout.addWidget(self.sep2, alignment=Qt.AlignmentFlag.AlignBottom)
		
		self.misc_layout = QHBoxLayout()

		self.settings_btn = QPushButton(tr('mainwnd_settings'), self)
		self.settings_btn.setFixedHeight(self.height() // 8)
		self.settings_btn.setFixedWidth(self.width() * 23 // 120)
		self.misc_layout.addWidget(self.settings_btn)

		self.about_btn = QPushButton(tr('mainwnd_about'), self)
		self.about_btn.setFixedHeight(self.height() // 8)
		self.about_btn.setFixedWidth(self.width() * 23 // 120)
		self.misc_layout.addWidget(self.about_btn)
		self.misc_layout.setSpacing(self.width() // 60)

		self.tools_layout.addLayout(self.misc_layout)

		self.misc_label = QLabel(tr('version_text', ver=VERSION) + '. <a href="hide_wnd">' + tr('mainwnd_hide') + '</a>', self)
		tmp_font.setPointSize(tmp_font.pointSize() * 9 // 10)
		self.misc_label.setFont(tmp_font)
		self.misc_label.setOpenExternalLinks(False)
		self.tools_layout.addWidget(self.misc_label, alignment=Qt.AlignmentFlag.AlignHCenter)
		self.tools_layout.setSpacing(self.height() // 40)
		self.tools_layout.setContentsMargins(10, 0, 10, 0)

		self.main_layout.addWidget(self.tools_widget, alignment=Qt.AlignmentFlag.AlignCenter, stretch=0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setCentralWidget(self.main_widget)

		self.initial = True

		self.cur_idx = ''
		self.cur_name = ''
		self.cur_weight = 0
		self.cur_chance = 0

	def upd_wndflags(self):
		if int(l('stay_on_top', 1)) and not self.on_top:
			self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
			self.on_top = 1
		if not int(l('stay_on_top', 1)) and self.on_top:
			self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
			self.on_top = 0

		self.show()
		lgr.info('Main window flags updated')

	def reload_lang(self):
		self.step_btn.setText(tr('mainwnd_step'))
		self.start_btn.setText(tr('mainwnd_start'))
		self.settings_btn.setText(tr('mainwnd_settings'))
		self.about_btn.setText(tr('mainwnd_about'))
		if self.width() <= 400:
			self.misc_label.setText('<a href="hide_wnd">' + tr('mainwnd_hide') + '</a>')
		else:
			self.misc_label.setText(tr('version_text', ver=VERSION) + '. <a href="hide_wnd">' + tr('mainwnd_hide') + '</a>')

		if self.initial:
			self.nn_widget.setToolTip('')
		else:
			self.nn_widget.setToolTip(tr('mainwnd_tooltip', idx=self.cur_idx, name=self.cur_name, weight=self.cur_weight, chance=self.cur_chance))

		self.hiddenwnd.setText(tr('hidewnd_text'))
		self.aboutwnd.reload_lang()

	def reload_settings(self):
		if not int(l('wnd_behavior', 0)):
			self.setFixedSize(l('initsz', g()))
		else:
			self.setMinimumSize(QSize(0, 0))
			self.setMaximumSize(QSize(16777215, 16777215))
			self.resize(l('initsz', g()))
		self.resize_widgets()
		lgr.info('Main window settings reloaded')

	def resize_widgets(self):
		self.number_label.setFont(QFont('Consolas', self.height() // 2))
		tmp_font = self.name_label.font()
		tmp_font.setPointSize(self.height() // 6)
		self.name_label.setFont(tmp_font)
		self.step_btn.setFixedWidth(self.width() * 2 // 5)
		self.step_btn.setFixedHeight(self.height() // 3)
		tmp_font = self.step_btn.font()
		tmp_font.setPointSize(self.height() // 20)
		self.step_btn.setFont(tmp_font)
		self.start_btn.setFixedWidth(self.width() * 2 // 5)
		self.start_btn.setFixedHeight(self.height() // 3)
		self.start_btn.setFont(tmp_font)
		tmp_font.setPointSize(self.height() // 25)
		self.settings_btn.setFixedHeight(self.height() // 8)
		self.about_btn.setFixedHeight(self.height() // 8)
		self.settings_btn.setFixedWidth(self.width() * 23 // 120)
		self.about_btn.setFixedWidth(self.width() * 23 // 120)
		self.settings_btn.setFont(tmp_font)
		self.about_btn.setFont(tmp_font)
		self.misc_layout.setSpacing(self.width() // 60)
		self.tools_layout.setSpacing(self.height() // 40)
		tmp_font.setPointSize(tmp_font.pointSize() * 9 // 10)
		self.misc_label.setFont(tmp_font)
		if self.width() <= 400:
			self.misc_label.setText('<a href="hide_wnd">' + tr('mainwnd_hide') + '</a>')
		else:
			self.misc_label.setText(tr('version_text', ver=VERSION) + '. <a href="hide_wnd">' + tr('mainwnd_hide') + '</a>')

		self.number_label.home(False)
		self.name_label.home(False)

	def hidebtn_clicked(self, link: str):
		lgr.info('Hide window activated')
		if PLATFORM == 'Linux':
			lgr.warning('Running on Linux. The hidden window position may not be correct')
		self.hiddenwnd.show()
		self.hide()
	
	def update_nn(self, idx, name, weight, chance):
		self.number_label.setText(str(idx))
		self.name_label.setText(str(name))
		self.nn_widget.setToolTip(tr('mainwnd_tooltip', idx=idx, name=name, weight=weight, chance=chance))
		
		self.cur_idx = idx
		self.cur_name = name
		self.cur_weight = weight
		self.cur_chance = chance
		self.initial = False

		self.name_label.home(False)
		self.number_label.home(False)

	def connect_signals(self):
		self.step_btn.clicked.connect(self.random_engine.step)
		self.start_btn.clicked.connect(self.random_engine.toggle)
		self.misc_label.linkActivated.connect(self.hidebtn_clicked)
		self.settings_btn.clicked.connect(self.on_settings)
		self.about_btn.clicked.connect(self.aboutwnd.exec)

	def on_settings(self):
		self.settings_wnd.reload_settings()
		self.settings_wnd.exec()