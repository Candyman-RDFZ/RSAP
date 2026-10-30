from PySide6.QtCore import QSettings
from core.config import NAME, ORG

import logging
lgr = logging.getLogger(__name__)

settings = QSettings(ORG, NAME)

def save(key: str, value):
	global settings
	lgr.info(f'Saved settings {key} to {value}')
	settings.setValue(key, value)

def load(key: str, default):
	global settings
	if not settings.contains(key):
		lgr.info(f'Settings {key} does not yet exist. Setting to default value {default}')
		save(key, default)
	return settings.value(key)
