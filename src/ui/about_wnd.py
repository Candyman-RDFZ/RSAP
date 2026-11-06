from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QSizePolicy, QMessageBox, QLayout

from core.config import VERSION, FULL_NAME
from core.utils import get_about_wnd_dimension as g
from core.utils import sanitize_path as p
from core.update_checker import UpdateChecker

import json

class RSAPAboutWnd(QDialog):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.setWindowTitle('About RSAP')
		self.setFixedSize(g())
		self.updchk = UpdateChecker(self.parent)

		self.layout = QVBoxLayout()

		self.logo = QPixmap(p('logo.png'))
		self.logo = self.logo.scaledToWidth(self.width() // 2, Qt.SmoothTransformation)
		self.logo_lbl = QLabel()
		self.logo_lbl.setPixmap(self.logo)
		self.layout.addWidget(self.logo_lbl, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

		self.lbl = QLabel(f"<center>{FULL_NAME}. <a href=\"chkupd\">Check for Updates</a>.</center><p><b>RSAP (Randomly Select a Person)</b> is a free, powerful, and cross-platform tool for random selection. Despite being originally designed for selecting random people in classrooms, its high customizability allows it to be used in almost all scenarios involving random selection, such as the lottery.</p><p>Copyright &copy; 2026 <a href=\"https://candyman33.cc/\">Candy_man</a>.<br>This program comes with ABSOLUTELY NO WARRANTY.<br>This is free software, and you are welcome to redistribute it under certain conditoins. See the <a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">GNU General Public License</a> for more details.</p><p>For more information and help on using, please refer to the following links:<center>Website: <a href=\"https://candyman33.cc/p/RSAP/\">https://candyman33.cc/p/RSAP/</a><br>Help: <a href=\"https://candyman33.cc/p/RSAP/h/\">https://candyman33.cc/p/RSAP/h/</a><br>Source code: <a href=\"https://github.com/Candyman-RDFZ/RSAP/\">GitHub</a> | <a href=\"https://gitee.com/Candyman-RDFZ/RSAP/\">Gitee</a><br><b>Donate!</b>&nbsp;&nbsp;<a href=\"https://candyman33.cc/donate\">https://candyman33.cc/donate</a></center></p>")
		self.lbl.setWordWrap(True)
		self.lbl.setOpenExternalLinks(False)
		self.lbl.linkActivated.connect(self.on_click)
		self.lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.layout.addWidget(self.lbl, stretch=1)

		self.setLayout(self.layout)
		self.layout.setSizeConstraint(QLayout.SetFixedSize)

	def on_click(self, link):
		if link != 'chkupd':
			QDesktopServices.openUrl(QUrl(link))
			return
		self.updchk.chk(self.on_finished)

	def on_finished(self, text):
		if text == -1:
			dialog = QMessageBox(self.parent)
			dialog.setWindowTitle('Error - RSAP')
			dialog.setText('<p>Failed to check for updates. Please check your internet connection, and try again.</p><p>If you believe the problem is not with your internet, please contact me at dckx18@gmail.com</p>')
			dialog.setIcon(QMessageBox.Critical)
			dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Retry)
			res = dialog.exec()
			if res == QMessageBox.Retry:
				self.updchk.chk(self.on_finished)
			return
		text = json.loads(text)
		ver = text['ver']
		if ver == VERSION:
			QMessageBox.information(self, 'Info - RSAP', f'RSAP is already the newest version ({VERSION}).', buttons=QMessageBox.Ok)
			return
		changes = text['changes']
		dialog = QMessageBox(self)
		dialog.setWindowTitle('Info - RSAP')
		dialog.setText(f'<p>A newer version of RSAP ({ver}) was found. (The current version is {VERSION})</p><p>Changes in the newest version include:{changes}</p><p>You can download the newest version at <a href=\"https://candyman33.cc/p/RSAP/d/{ver}/\">https://candyman33.cc/p/RSAP/d/{ver}/</a>')
		dialog.setIcon(QMessageBox.Information)
		dialog.setStandardButtons(QMessageBox.Open | QMessageBox.Ok)
		res = dialog.exec()
		if res == QMessageBox.Open:
			QDesktopServices.openUrl(QUrl(f'https://candyman33.cc/p/RSAP/d/{ver}/'))
