from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QLabel, QPushButton

class UpdchkDialog(QMessageBox):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		
		self.setWindowTitle('Checking - RSAP')
		self.setIcon(QMessageBox.Information)
		self.setText('Checking for updates. Please wait...')

		self.abort_btn = QPushButton('Abort')
		self.abort_btn.clicked.connect(self.abort)
		self.addButton(self.abort_btn, QMessageBox.ButtonRole.RejectRole)

	def closeEvent(self, event):
		event.ignore()

	def reject(self):
		pass

	def abort(self):
		self.parent.updchk.abort()
		self.force_close()

	def force_close(self):
		super().reject()