from PySide6.QtCore import Qt, QSize, QRegularExpression, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QGroupBox, QButtonGroup, QRadioButton, QCheckBox, QLineEdit, QMessageBox, QSpinBox
from PySide6.QtGui import QRegularExpressionValidator

from core.utils import get_settings_wnd_dimension as g, get_window_dimension as gw
from core.settings import save as s, load as l

from ui.name_table import NameTableWidget

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
		self.apply = QPushButton('Apply')
		self.help = QPushButton('Help')

		self.buttons_layout.addWidget(self.help, alignment=Qt.AlignmentFlag.AlignLeft)
		self.buttons_layout.addStretch()
		self.buttons_layout.addWidget(self.ok, alignment=Qt.AlignmentFlag.AlignRight)
		self.buttons_layout.addWidget(self.cancel, alignment=Qt.AlignmentFlag.AlignRight)
		self.buttons_layout.addWidget(self.apply, alignment=Qt.AlignmentFlag.AlignRight)

		self.ok.setDefault(True)
		self.ok.clicked.connect(self.ok_callback)
		self.apply.clicked.connect(self.save_settings)
		self.cancel.clicked.connect(self.close)
		self.help.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://candyman33.cc/p/RSAP/h/')))

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

		self.autostop_settings = QGroupBox('Auto Stop')
		self.autostop_layout = QVBoxLayout()
		self.autostop_settings.setLayout(self.autostop_layout)
		self.general_layout.addWidget(self.autostop_settings)

		self.ats_num_layout = QHBoxLayout()
		self.ats_num_lbl = QLabel('Auto stop after selecting ')
		self.ats_num_layout.addWidget(self.ats_num_lbl)
		self.ats_num = QSpinBox()
		self.ats_num.setSuffix(' person(s)')
		self.ats_num.setRange(1, 500)
		self.ats_num.setSingleStep(1)
		self.ats_num.setValue(int(l('ats_num', 20)))
		self.ats_num_layout.addWidget(self.ats_num)
		self.autostop_layout.addLayout(self.ats_num_layout)

		self.ats_time_layout = QHBoxLayout()
		self.ats_time_lbl = QLabel('Delay between each selection: ')
		self.ats_time_layout.addWidget(self.ats_time_lbl)
		self.ats_time = QSpinBox()
		self.ats_time.setSuffix(' milliseconds')
		self.ats_time.setRange(10, 1000)
		self.ats_time.setSingleStep(10)
		self.ats_time.setValue(int(l('ats_time', 100)))
		self.ats_time_layout.addWidget(self.ats_time)
		self.autostop_layout.addLayout(self.ats_time_layout)

		self.antirep_settings = QGroupBox('Anti-Repetition')
		self.antirep_layout_ = QVBoxLayout()
		self.antirep_settings.setLayout(self.antirep_layout_)
		self.general_layout.addWidget(self.antirep_settings)
		
		self.antirep_enabled = int(l('antirep_enabled', 1))
		self.antirep_chk = QCheckBox('Enable anti-repetition')
		self.antirep_chk.setChecked(self.antirep_enabled)
		self.antirep_chk.checkStateChanged.connect(self.antirep_changed)
		self.antirep_layout_.addWidget(self.antirep_chk)

		self.antirep_layout = QHBoxLayout()
		self.antirep_layout_.addLayout(self.antirep_layout)
		self.antirep_lbl = QLabel('Do not repeat for ')
		self.antirep_layout.addWidget(self.antirep_lbl)

		self.antirep_num = int(l('antirep_num', 2)) # TODO: change this to len(data) // 2
		self.antirep_numspn = QSpinBox()
		self.antirep_numspn.setRange(1, 4) # TODO: change this to len(data)
		self.antirep_numspn.setSingleStep(1)
		self.antirep_numspn.setValue(self.antirep_num if self.antirep_enabled else 1)
		self.antirep_numspn.setSuffix(' person(s)')
		self.antirep_numspn.setEnabled(self.antirep_enabled)
		self.antirep_layout.addWidget(self.antirep_numspn)

		self.antirep_note = QLabel('<b>Note</b>: Setting 1 is the same as disabling.')
		self.antirep_note.setFont(tmp_font)
		self.antirep_layout_.addWidget(self.antirep_note)

		self.ie_settings = QGroupBox('Import/Export')
		self.ie_layout = QHBoxLayout()
		self.ie_settings.setLayout(self.ie_layout)
		self.general_layout.addWidget(self.ie_settings)

		self.ie_lbl = QLabel('Export settings file from you current settings that can be imported on a different machine.')
		self.ie_lbl.setWordWrap(True)
		self.ie_layout.addWidget(self.ie_lbl)

		self.ie_btn = QVBoxLayout()
		self.import_btn = QPushButton('Import')
		self.ie_btn.addWidget(self.import_btn)
		self.export_btn = QPushButton('Export')
		self.ie_btn.addWidget(self.export_btn)
		self.ie_layout.addLayout(self.ie_btn)

		self.general_layout.addStretch()

		# --------------------------------

		self.name_layout_ = QVBoxLayout()
		self.name_widget.setLayout(self.name_layout_)

		self.name_warn = QLabel('<b>Warning</b>: Be sure to press the "Apply" button at the bottom before going back to the "General" tab to make further changes.')
		self.name_warn.setWordWrap(True)
		self.name_layout_.addWidget(self.name_warn)

		self.name_wdg = QWidget()
		self.name_layout = QHBoxLayout()
		self.name_wdg.setLayout(self.name_layout)

		self.btns_layout = QVBoxLayout()
		self.btns_widget = QWidget()
		self.btns_widget.setLayout(self.btns_layout)

		self.add_btn = QPushButton('Add')
		self.edit_btn = QPushButton('Edit')
		self.del_btn = QPushButton('Delete')
		self.btns_layout.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignTop)
		self.btns_layout.addWidget(self.edit_btn, alignment=Qt.AlignmentFlag.AlignTop)
		self.btns_layout.addWidget(self.del_btn, alignment=Qt.AlignmentFlag.AlignTop)

		self.name_table = NameTableWidget(self.add_btn, self.edit_btn, self.del_btn, self)
		self.name_table.set_value(self.parent.random_engine.data)
		self.name_layout.addWidget(self.name_table)
		self.name_layout.addWidget(self.btns_widget, alignment=Qt.AlignmentFlag.AlignTop)

		self.name_layout_.addWidget(self.name_wdg, alignment=Qt.AlignmentFlag.AlignHCenter, stretch=1)

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

	def antirep_changed(self, state):
		self.antirep_enabled = self.antirep_chk.isChecked()
		if self.antirep_enabled:
			self.antirep_numspn.setValue(self.antirep_num)
		else:
			self.antirep_num = self.antirep_numspn.value()
			self.antirep_numspn.setValue(1)
		self.antirep_numspn.setEnabled(self.antirep_enabled)

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

		s('ats_num', self.ats_num.value())
		s('ats_time', self.ats_time.value())

		s('antirep_enabled', int(self.antirep_enabled))
		s('antirep_num', self.antirep_num)

		self.parent.reload_settings()
		self.parent.random_engine.reload_settings()
	
	def ok_callback(self):
		self.save_settings()
		self.close()