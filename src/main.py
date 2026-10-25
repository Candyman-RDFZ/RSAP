from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from core.config import NAME, ORG, FULL_NAME, PLATFORM, EXEC, ID
from core.utils import sanitize_path as p
from ui.main_window import RSAPMainWindow
from core.logs.setup_log import setup_logging

import sys
import logging

setup_logging()

lgr = logging.getLogger(__name__)

lgr.info('==================================')
lgr.info(FULL_NAME)
lgr.info(f'Platform: {PLATFORM}')
lgr.info(f'Running as: {'executable' if EXEC else 'source code'}')

if PLATFORM == 'Windows':
	lgr.info('Running on Windows. Trying to set model ID...')
	try:
		from ctypes import windll
		windll.shell32.SetCurrentProcessExplicitAppUserModelID(ID)
	except Exception as e:
		lgr.error(e)
		lgr.warning('Failed to set model ID. The icon on the taskbar may show incorrectly')
	else:
		lgr.info('Successfully set model ID')

elif PLATFORM == 'Linux':
	lgr.info('Running on Linux. Forcing X11...')
	try:
		import os
		os.environ['QT_QPA_PLATFORM'] = 'xcb'
	except Exception as e:
		lgr.error(e)
		lgr.warning('Failed to force X11. Window positions and flags may not be correct')
	else:
		lgr.info('Successfully forced X11')

app = QApplication([])
app.setApplicationName(NAME)
app.setOrganizationName(ORG)
app.setWindowIcon(QIcon(p('assets/icon.png')))

lgr.info('Created application')

RSAP = RSAPMainWindow()
RSAP.show()

sys.exit(app.exec())
