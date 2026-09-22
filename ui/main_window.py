from PySide6.QtWidgets import QMainWindow

from core.utils import get_window_dimension

class RSAPMainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('RSAP')
		self.setFixedSize(get_window_dimension())
