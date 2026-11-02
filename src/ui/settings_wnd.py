from PySide6.QtCore import Qt, QSize, QRegularExpression
from PySide6.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QGroupBox, QButtonGroup, QRadioButton, QCheckBox, QLineEdit, QMessageBox
from PySide6.QtGui import QRegularExpressionValidator

from core.utils import get_settings_wnd_dimension as g, get_window_dimension as gw
from core.settings import save as s, load as l

from random import randint
import logging

lgr = logging.getLogger(__name__)

class SettingsWnd(QDialog):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		lgr.info('Settings window initiated.')

		self.setFixedSize(g())
		self.setWindowTitle('Settings - RSAP')

		self.layout = QVBoxLayout(self)

		self.tabs = QTabWidget()
		self.general_widget = QWidget()
		self.name_widget = QWidget()
		self.tabs.addTab(self.general_widget, 'General')
		self.tabs.addTab(self.name_widget, 'Names && Chances')
		self.layout.addWidget(self.tabs)

		self.buttons_layout = QHBoxLayout()

		self.ok = QPushButton('OK')
		self.cancel = QPushButton('Cancel')
		self.import_btn = QPushButton('Import')
		self.export_btn = QPushButton('Export')

		self.buttons_layout.addWidget(self.import_btn, alignment=Qt.AlignmentFlag.AlignLeft)
		self.buttons_layout.addWidget(self.export_btn, alignment=Qt.AlignmentFlag.AlignLeft)
		self.buttons_layout.addStretch()
		self.buttons_layout.addWidget(self.ok, alignment=Qt.AlignmentFlag.AlignRight)
		self.buttons_layout.addWidget(self.cancel, alignment=Qt.AlignmentFlag.AlignRight)

		self.ok.setDefault(True)
		self.ok.clicked.connect(self.save_settings)
		self.cancel.clicked.connect(self.close)

		self.layout.addLayout(self.buttons_layout)

		self.general_layout = QVBoxLayout()
		self.general_widget.setLayout(self.general_layout)

		self.wnd_settings = QGroupBox('Window')
		self.wnd_layout = QVBoxLayout()
		self.wnd_settings.setLayout(self.wnd_layout)
		self.general_layout.addWidget(self.wnd_settings)
		
		self.wnd_behavior_layout = QHBoxLayout()
		self.wnd_behavior = QLabel('Behavior: ')
		self.wnd_behavior_layout.addWidget(self.wnd_behavior)
		self.wnd_bg = QButtonGroup()

		for txt in ['Fixed', 'Resizable']:
			rb = QRadioButton(txt)
			self.wnd_bg.addButton(rb)
			self.wnd_behavior_layout.addWidget(rb)
		self.wnd_bg.buttons()[int(l('wnd_behavior', 0))].setChecked(True)
		self.wnd_behavior_layout.addStretch()
		self.sot_chk = QCheckBox('Stay on top')
		self.sot_chk.setChecked(int(l('stay_on_top', 1)))
		self.wnd_behavior_layout.addWidget(self.sot_chk)

		self.wnd_behavior_layout.setSpacing(0)
		self.wnd_layout.addLayout(self.wnd_behavior_layout)

		self.wnd_initsz_layout = QHBoxLayout()
		self.initsz_lbl = QLabel('Initial size:')
		self.wnd_initsz_layout.addWidget(self.initsz_lbl)

		self.initsz_x = QLineEdit()
		self.initsz_wd = QLabel('Width:')
		self.initsz_x.setMaxLength(4)
		self.initsz_x.setValidator(QRegularExpressionValidator(QRegularExpression(r'[0-9]{1,4}'), self.initsz_x))
		self.initsz_x.setText(str(l('initsz', gw()).width()))
		self.wnd_initsz_layout.addWidget(self.initsz_wd)
		self.wnd_initsz_layout.addWidget(self.initsz_x)

		self.initsz_y = QLineEdit()
		self.initsz_he = QLabel('Height:')
		self.initsz_y.setPlaceholderText('Height')
		self.initsz_y.setMaxLength(4)
		self.initsz_x.setValidator(QRegularExpressionValidator(QRegularExpression(r'[0-9]{1,4}'), self.initsz_y))
		self.initsz_y.setText(str(l('initsz', gw()).height()))
		self.wnd_initsz_layout.addWidget(self.initsz_he)
		self.wnd_initsz_layout.addWidget(self.initsz_y)

		self.wnd_layout.addLayout(self.wnd_initsz_layout)

		self.seed_settings = QGroupBox('Seed')
		self.seed_layout_ = QVBoxLayout()
		self.seed_layout = QHBoxLayout()
		self.seed_settings.setLayout(self.seed_layout_)
		self.general_layout.addWidget(self.seed_settings)

		self.seed_type_lbl = QLabel('Type:')
		self.seed_layout.addWidget(self.seed_type_lbl)

		self.seed_bg = QButtonGroup()
		self.seed_type = int(l('seed_type', 0))
		self.cur_seed = l('rand_seed', randint(0, int(1e15)))

		for txt in ['Random', 'Custom']:
			rb = QRadioButton(txt)
			self.seed_bg.addButton(rb)
			self.seed_layout.addWidget(rb)
		self.seed_bg.buttons()[self.seed_type].setChecked(True)
		self.seed_bg.idClicked.connect(self.seed_btn_changed)

		self.seed_entry = QLineEdit()
		self.seed_entry.setValidator(QRegularExpressionValidator(QRegularExpression(r'[0-9]{1,15}'), self.seed_entry))
		self.seed_entry.setText(str(self.cur_seed) if self.seed_type else '<Random>')
		self.seed_entry.setEnabled(self.seed_type)
		self.seed_layout.addWidget(self.seed_entry)

		self.seed_layout_.addLayout(self.seed_layout)

		self.seed_warn = QLabel('<b>Warning</b>: Only use custom seeds for testing purposes. Setting a custom seed will cause the program to generate the same selection sequence each time.')
		self.seed_warn.setWordWrap(True)
		tmp_font = self.seed_warn.font()
		tmp_font.setPointSize(self.height() // 80)
		self.seed_warn.setFont(tmp_font)
		self.seed_layout_.addWidget(self.seed_warn)

		self.general_layout.addStretch()

	def seed_btn_changed(self, button_id):
		self.seed_type = self.seed_bg.buttons()[1].isChecked()
		if self.seed_type:
			self.seed_entry.setText(str(self.cur_seed))
		else:
			try:
				self.cur_seed = int(self.seed_entry.text())
			except: pass
			self.seed_entry.setText('<Random>')
		self.seed_entry.setEnabled(self.seed_type)

	def chk_initsz(self) -> bool:
		self.sz_x = int(self.initsz_x.text())
		self.sz_y = int(self.initsz_y.text())
		if 100 <= self.sz_x <= 2000 and 100 <= self.sz_y <= 2000:
			return True
		QMessageBox.critical(self, 'Error', 'The initial size must be between 100x100 and 2000x2000.')
		return False

	def save_settings(self):
		s('wnd_behavior', int(self.wnd_bg.buttons()[1].isChecked()))
		s('stay_on_top', int(self.sot_chk.isChecked()))
		
		if not self.chk_initsz():
			return
		s('initsz', QSize(int(self.initsz_x.text()), int(self.initsz_y.text())))

		s('seed_type', int(self.seed_bg.buttons()[1].isChecked()))
		if self.seed_type:
			self.cur_seed = self.seed_entry.text()
		s('rand_seed', int(self.cur_seed))

		self.parent.reload_settings()
		self.parent.random_engine.reload_settings()
		self.close()
