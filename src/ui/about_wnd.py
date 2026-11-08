from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QSizePolicy, QMessageBox, QLayout

from core.config import VERSION
from core.utils import get_about_wnd_dimension as g
from core.utils import sanitize_path as p
from core.update_checker import UpdateChecker
from ui.updchk_dialog import UpdchkDialog
from core.translator import tr

import json

class RSAPAboutWnd(QDialog):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.setWindowTitle(tr('mainwnd_about') + ' RSAP')
		self.setFixedSize(g())

		self.updchk_dialog = UpdchkDialog(self)
		self.updchk = UpdateChecker(self)
		self.updchk.finished.connect(self.on_finished)
		self.updchk.error.connect(self.on_error)

		self.layout = QVBoxLayout()

		self.logo = QPixmap(p('logo.png'))
		self.logo = self.logo.scaledToWidth(self.width() // 2, Qt.SmoothTransformation)
		self.logo_lbl = QLabel()
		self.logo_lbl.setPixmap(self.logo)
		self.layout.addWidget(self.logo_lbl, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

		self.lbl = QLabel(tr('about_text', ver=VERSION))
		self.lbl.setWordWrap(True)
		self.lbl.setOpenExternalLinks(False)
		self.lbl.linkActivated.connect(self.on_click)
		self.lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
		self.layout.addWidget(self.lbl, stretch=1)

		self.setLayout(self.layout)
		self.layout.setSizeConstraint(QLayout.SetFixedSize)

	def reload_lang(self):
		self.setWindowTitle(tr('mainwnd_about') + ' RSAP')
		self.lbl.setText(tr('about_text', ver=VERSION))
		self.updchk_dialog.reload_lang()

	def on_click(self, link):
		if link != 'chkupd':
			QDesktopServices.openUrl(QUrl(link))
			return
		self.updchk_dialog.show()
		self.updchk.chk()

	def on_finished(self, text):
		self.updchk_dialog.force_close()
		text = json.loads(text)
		ver = text['ver']
		if ver <= VERSION:
			dialog = QMessageBox(self)
			dialog.setWindowTitle(tr('updchk_info') + ' - RSAP')
			dialog.setIcon(QMessageBox.Information)
			dialog.setText(tr('updchk_newest', version=VERSION))
			ok_btn = dialog.addButton(tr('stgwnd_ok'), QMessageBox.ButtonRole.AcceptRole)
			dialog.exec()
			return
		changes = text['changes']
		dialog = QMessageBox(self)
		dialog.setWindowTitle(tr('updchk_info') + ' - RSAP')
		dialog.setText(tr('updchk_old', newver=ver, oldver=VERSION, changes=changes))
		dialog.setIcon(QMessageBox.Information)
		ok_btn = dialog.addButton(tr('stgwnd_ok'), QMessageBox.ButtonRole.RejectRole)
		open_btn = dialog.addButton(tr('updchk_open'), QMessageBox.ButtonRole.AcceptRole)
		dialog.exec()
		if dialog.clickedButton() == open_btn: 
			QDesktopServices.openUrl(QUrl(f'https://candyman33.cc/p/RSAP/d/{ver}/'))

	def on_error(self, text):
		self.updchk_dialog.force_close()
		dialog = QMessageBox(self)
		dialog.setWindowTitle(tr('updchk_error') + ' - RSAP')
		dialog.setText(tr('updchk_errtext', text=text))
		dialog.setIcon(QMessageBox.Critical)
		close_btn = dialog.addButton(tr('updchk_close'), QMessageBox.ButtonRole.RejectRole)
		retry_btn = dialog.addButton(tr('updchk_retry'), QMessageBox.ButtonRole.AcceptRole)
		dialog.exec()
		if dialog.clickedButton() == retry_btn:
			self.updchk.chk()