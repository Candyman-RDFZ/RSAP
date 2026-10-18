from PySide6.QtWidgets import QDialog
from core.utils import get_settings_wnd_dimension as g

import logging

lgr = logging.getLogger(__name__)

class SettingsWnd(QDialog):
	def __init__(self, parent):
		super().__init__(parent)

		lgr.info('Settings window initiated.')

		self.setFixedSize(g())
		self.setWindowTitle('Settings - RSAP')
