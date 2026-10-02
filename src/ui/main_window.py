from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QPushButton, QSizePolicy, QCheckBox, QLineEdit

from core.utils import get_window_dimension
from core.config import PLATFORM
from ui.hidden_wnd import RSAPHiddenWnd

import logging

lgr = logging.getLogger(__name__)

class RSAPMainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		lgr.info('Main window initiated')
		if PLATFORM == 'Linux':
			lgr.warning('Running on Linux. Some window features, such as stay on top, may not function correctly')

		self.setWindowFlags(Qt.WindowStaysOnTopHint & ~Qt.WindowType.WindowMaximizeButtonHint)

		self.hiddenwnd = RSAPHiddenWnd(self)

		self.setWindowTitle('RSAP')
		self.resize(get_window_dimension())
		lgr.info('Window parameters set')

		self.setup_ui()
		lgr.info('Main UI is now set up')

		self.connect_signals()
		lgr.info('Signals are now connected')

	def setup_ui(self):
		self.main_layout = QHBoxLayout()
		self.main_widget = QWidget()
		self.main_widget.setLayout(self.main_layout)

		self.nn_layout = QVBoxLayout()
		self.nn_widget = QWidget()
		self.nn_widget.setLayout(self.nn_layout)

		self.number_label = QLabel('??', self)
		self.number_label.setFont(QFont('Consolas', self.height() // 2))
		self.number_label.setStyleSheet('color: #0094FF; font-weight: bold;')
		self.nn_layout.addWidget(self.number_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
		
		self.name_label = QLabel('', self)
		tmp_font = self.name_label.font()
		tmp_font.setPointSize(self.height() // 6)
		self.name_label.setFont(tmp_font)
		self.nn_layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

		self.main_layout.addWidget(self.nn_widget, alignment=Qt.AlignmentFlag.AlignLeft)

		self.sep1 = QFrame()
		self.sep1.setFrameShape(QFrame.VLine)
		self.main_layout.addWidget(self.sep1, alignment=Qt.AlignmentFlag.AlignLeft)

		self.tools_layout = QVBoxLayout()
		self.tools_widget = QWidget()
		self.tools_widget.setLayout(self.tools_layout)

		self.step_btn = QPushButton('Step', self)
		self.step_btn.setFixedWidth(self.width() // 2)
		self.step_btn.setFixedHeight(self.height() // 5)
		tmp_font = self.step_btn.font()
		tmp_font.setPointSize(self.height() // 20)
		self.tools_layout.addWidget(self.step_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.start_btn = QPushButton('Start', self)
		self.start_btn.setFixedWidth(self.width() // 2)
		self.start_btn.setFixedHeight(self.height() // 5)
		self.tools_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.autostop_chk = QCheckBox('Auto Stop', self)
		self.tools_layout.addWidget(self.autostop_chk, alignment=Qt.AlignmentFlag.AlignHCenter)
		
		self.adup_chk = QCheckBox('Anti-duplication', self)
		self.tools_layout.addWidget(self.adup_chk, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.sep2 = QFrame()
		self.sep2.setFrameShape(QFrame.HLine)
		self.tools_layout.addWidget(self.sep2, alignment=Qt.AlignmentFlag.AlignBottom)
		
		self.misc_layout = QHBoxLayout()

		self.settings_btn = QPushButton('Settings', self)
		self.misc_layout.addWidget(self.settings_btn)

		self.about_btn = QPushButton('About', self)
		self.misc_layout.addWidget(self.about_btn)
		self.misc_layout.setSpacing(self.height() // 30)

		self.tools_layout.addLayout(self.misc_layout)

		self.misc_label = QLabel('RSAP version 0.0pre. <a href="hide_wnd">Hide Window</a>', self)
		self.misc_label.setOpenExternalLinks(False)
		self.misc_label.linkActivated.connect(self.hidebtn_clicked)
		self.tools_layout.addWidget(self.misc_label, alignment=Qt.AlignmentFlag.AlignHCenter)
		self.tools_layout.setSpacing(self.height() // 40)

		self.main_layout.addWidget(self.tools_widget, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(0)
		self.setCentralWidget(self.main_widget)

	def hidebtn_clicked(self, link: str):
		lgr.info('Hide window activated')
		if PLATFORM == 'Linux':
			lgr.warning('Running on Linux. The hidden window position may not be correct')
		self.hiddenwnd.show()
		self.hide()
	
	def connect_signals(self): pass
