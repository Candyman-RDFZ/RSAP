from PySide6.QtCore import QSize
from PySide6.QtGui import QGuiApplication

def get_window_dimension() -> QSize:
	screen = QGuiApplication.primaryScreen()
	width = screen.size().width() // 3
	height = width // 2
	return QSize(width, height)
