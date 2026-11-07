from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QLabel, QPushButton

from core.translator import tr

class UpdchkDialog(QMessageBox):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		
		self.setWindowTitle(tr('updchk_chk') + ' - RSAP')
		self.setIcon(QMessageBox.Information)
		self.setText(tr('updchk_chking'))

		self.abort_btn = QPushButton(tr('updchk_abrt'))
		self.abort_btn.clicked.connect(self.abort)
		self.addButton(self.abort_btn, QMessageBox.ButtonRole.RejectRole)

	def reload_lang(self):
		self.setWindowTitle(tr('updchk_chk') + ' - RSAP')
		self.setText(tr('updchk_chking'))
		self.abort_btn.setText(tr('updchk_abrt'))

	def closeEvent(self, event):
		event.ignore()

	def reject(self):
		pass

	def abort(self):
		self.parent.updchk.abort()
		self.force_close()

	def force_close(self):
		super().reject()