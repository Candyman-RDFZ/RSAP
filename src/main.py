from PySide6.QtWidgets import QApplication

from core.config import NAME, ORG
from ui.main_window import RSAPMainWindow

import sys

app = QApplication([])
app.setApplicationName(NAME)
app.setOrganizationName(ORG)

RSAP = RSAPMainWindow()
RSAP.show()

sys.exit(app.exec())
