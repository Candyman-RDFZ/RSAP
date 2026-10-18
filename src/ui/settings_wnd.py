from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout, QPushButton

from core.utils import get_settings_wnd_dimension as g

import logging

lgr = logging.getLogger(__name__)

class SettingsWnd(QDialog):
	def __init__(self, parent):
		super().__init__(parent)

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
		self.cancel.clicked.connect(self.close)

		self.layout.addLayout(self.buttons_layout)
