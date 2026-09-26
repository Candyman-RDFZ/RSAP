from PySide6.QtCore import QSize
from PySide6.QtGui import QGuiApplication

def get_window_dimension() -> QSize:
	screen = QGuiApplication.primaryScreen()
	width = screen.size().width() * 2 // 5
	height = width // 2
	return QSize(width, height)

def get_hidewnd_dimension() -> QSize:
	screen = QGuiApplication.primaryScreen()
	width = height = screen.geometry().height() - screen.availableGeometry().height()
	if width == 0:
		width = height = screen.size().width() // 25
	return QSize(width, height)

def get_hidewnd_pos(wnd_w: int, wnd_h: int) -> tuple:
	screen = QGuiApplication.primaryScreen()
	geom = screen.geometry()
	return (geom.x() + geom.width() - wnd_w, geom.y() + geom.height() - wnd_h)
