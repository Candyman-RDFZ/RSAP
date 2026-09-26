from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from core.utils import get_hidewnd_dimension, get_hidewnd_pos

class RSAPHiddenWnd(QPushButton):
	def __init__(self, parent):
		super().__init__('Show')
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setFixedSize(get_hidewnd_dimension())
		pos = get_hidewnd_pos(self.width(), self.height())
		print(pos)
		self.move(pos[0], pos[1])

		self.mainwnd = parent
		self.clicked.connect(self.reshow_mainwnd)
	
	def reshow_mainwnd(self):
		self.mainwnd.show()
		self.hide()
