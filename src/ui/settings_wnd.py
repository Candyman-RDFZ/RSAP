from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QGroupBox, QButtonGroup, QRadioButton, QCheckBox

from core.utils import get_settings_wnd_dimension as g
from core.settings import save as s, load as l

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

		self.general_layout.addStretch()

	def save_settings(self):
		s('wnd_behavior', int(self.wnd_bg.buttons()[1].isChecked()))
		s('stay_on_top', int(self.sot_chk.isChecked()))

		self.parent.reload_settings()
		self.parent.random_engine.reload_settings()
		self.close()
