from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from core.utils import get_window_dimension

class RSAPMainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('RSAP')
		self.setFixedSize(get_window_dimension())

		self.main_layout = QHBoxLayout()
		self.main_widget = QWidget()
		self.main_widget.setLayout(self.main_layout)

		self.nn_layout = QVBoxLayout()
		self.nn_widget = QWidget()
		self.nn_widget.setLayout(self.nn_layout)

		self.number_label = QLabel('??', self)
		self.number_label.setFont(QFont('Consolas', self.height() // 2))
		self.number_label.setStyleSheet('color: #0094FF')
		self.nn_layout.addWidget(self.number_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
		
		self.name_label = QLabel('啊阿来', self)
		tmp_font = self.name_label.font()
		tmp_font.setPointSize(self.height() // 6)
		self.name_label.setFont(tmp_font)
		self.nn_layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)

		self.main_layout.addWidget(self.nn_widget, alignment=Qt.AlignmentFlag.AlignLeft)

		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setSpacing(2)
		self.setCentralWidget(self.main_widget)
