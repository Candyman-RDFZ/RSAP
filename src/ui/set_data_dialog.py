"""A custom dialog when the user clickes the add/edit buttons on the start page."""

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout

from core.utils import get_dlg_dimension as g

class AddDialog(QDialog):
	def __init__(self, parent=None, edit_name='', doi_num=''):
		super().__init__(parent)
		self.setWindowTitle('Add person - RSAP')
		self.setFixedSize(g())
		self.index_edit = QLineEdit()
		self.name_edit = QLineEdit()
		self.weight_edit = QLineEdit()
		
		self.form = QFormLayout()
		self.form.addRow('Index: ', self.index_edit)
		self.form.addRow('Name: ', self.name_edit)
		self.form.addRow('Weight: ', self.weight_edit)
		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		
		self.layout = QVBoxLayout()
		self.layout.addLayout(self.form)
		self.layout.addWidget(self.buttons)
		self.setLayout(self.layout)
	
	def values(self) -> tuple:
		return (self.index_edit.text(), self.name_edit.text(), self.weight_edit.text())

class EditDialog(QDialog):
	def __init__(self, parent=None, edit=False, edit_name='', doi_num=''):
		super().__init__(parent)
		self.setWindowTitle(('Add' if not edit else 'Edit') + ' Reference - doi2ref')
		self.name_edit = QLineEdit()
		self.doi_edit = QLineEdit()

		if edit:
			self.name_edit.setText(edit_name)
			self.doi_edit.setText(doi_num)
		
		self.form = QFormLayout()
		self.form.addRow('Reference Name: ', self.name_edit)
		self.form.addRow('DOI Number: ', self.doi_edit)
		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		
		self.layout = QVBoxLayout()
		self.layout.addLayout(self.form)
		self.layout.addWidget(self.buttons)
		self.setLayout(self.layout)
	
	def values(self) -> tuple:
		return (self.name_edit.text(), self.doi_edit.text())