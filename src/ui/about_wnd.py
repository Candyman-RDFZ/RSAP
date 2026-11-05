from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QSizePolicy

from core.utils import get_about_wnd_dimension as g
from core.utils import sanitize_path as p

class RSAPAboutWnd(QDialog):
	def __init__(self, parent):
		super().__init__(parent)

		self.setWindowTitle('About RSAP')
		self.setFixedSize(g())

		self.layout = QVBoxLayout()

		self.logo = QPixmap(p('logo.png'))
		self.logo = self.logo.scaledToWidth(self.width() // 2)
		self.logo_lbl = QLabel()
		self.logo_lbl.setPixmap(self.logo)
		self.layout.addWidget(self.logo_lbl, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

		self.lbl = QLabel("<center>RSAP version 0.0pre. <a href=\"chkupd\">Check for Updates</a>.</center><p><b>RSAP (Randomly Select a Person)</b> is a powerful, free, and cross-platform tool for random selection. Despite being originally designed for selecting random people in classrooms, it's high customizability allows it to be used in almost all scenarios involving random selection, such as the lottery.</p><p>Copyright &copy; 2026 <a href=\"https://candyman33.cc/\">Candy_man</a>.<br>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License. See <a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">the GNU General Public License</a> fore more details.</p><p>For more information and help on using, please refer to the following links:<center>Website: <a href=\"https://candyman33.cc/p/RSAP/\">https://candyman33.cc/p/RSAP/</a><br>Help: <a href=\"https://candyman33.cc/p/RSAP/h/\">https://candyman33.cc/p/RSAP/h/</a><br>Source code: <a href=\"https://github.com/Candyman-RDFZ/RSAP/\">GitHub</a> | <a href=\"https://gitee.com/Candyman-RDFZ/RSAP/\">Gitee</a><br><b>Donate!</b>&nbsp;&nbsp;<a href=\"https://candyman33.cc/donate\">https://candyman33.cc/donate</a></center></p>")
		self.lbl.setWordWrap(True)
		self.lbl.setOpenExternalLinks(True)
		self.lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.layout.addWidget(self.lbl, stretch=1)
		self.layout.setContentsMargins(self.width() // 20, 0, self.width() // 20, 0)

		self.setLayout(self.layout)