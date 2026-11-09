from PySide6.QtCore import QSize
from PySide6.QtGui import QGuiApplication
import pathlib

from core.config import ASSETS_ROOT, LANG_ROOT

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
	geom = screen.availableGeometry()
	return (geom.x() + geom.width() - wnd_w, geom.y() + geom.height() - wnd_h)

def get_settings_wnd_dimension() -> QSize:
	screen = QGuiApplication.primaryScreen()
	width = int(screen.size().width() * 0.31)
	height = width * 3 // 2
	return QSize(width, height)

def get_about_wnd_dimension() -> QSize:
	screen = QGuiApplication.primaryScreen()
	width = int(screen.size().width() * 0.35)
	height = width
	return QSize(width, height)

def get_dlg_dimension() -> QSize():
	screen = QGuiApplication.primaryScreen()
	width = int(screen.size().width() * 0.31 * 0.6)
	height = screen.size().width() // 10
	return QSize(width, height)

def sanitize_path(path: str, lang=False) -> str:
	if not lang:
		return str(ASSETS_ROOT / path)
	else:
		return str(LANG_ROOT / path)