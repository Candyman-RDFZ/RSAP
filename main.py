from PySide6.QtWidgets import QApplication

from core.config import NAME, ORG
# from core.rand.engine import RandomEngine
from ui.main_window import RSAPMainWindow

import sys

# random_engine = RandomEngine()

app = QApplication([])
app.setApplicationName(NAME)
app.setOrganizationName(ORG)

RSAP = RSAPMainWindow()
RSAP.show()

sys.exit(app.exec())
