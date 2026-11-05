"""A custom dialog when the user clickes the add/edit buttons on the start page."""

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout

from core.utils import get_dlg_dimension as g

class AddDialog(QDialog):
	def __init__(self, parent, default_weight):
		super().__init__(parent)
		self.setWindowTitle('Add person - RSAP')
		self.setFixedSize(g())
		self.index_edit = QLineEdit()
		self.name_edit = QLineEdit()
		self.weight_edit = QLineEdit()
		self.weight_edit.setText(str(default_weight))
		
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
	def __init__(self, parent, idxs, names, default_weight, multi: bool):
		super().__init__(parent)
		self.multi = multi
		self.setWindowTitle('Edit person - RSAP')
		self.setFixedSize(g())
		self.index_edit = QLineEdit()
		self.name_edit = QLineEdit()
		self.weight_edit = QLineEdit()
		if not multi:
			self.weight_edit.setText(str(default_weight))
		
		self.form = QFormLayout()
		self.form.addRow('Index: ', self.index_edit)
		self.form.addRow('Name: ', self.name_edit)
		self.form.addRow('Weight: ', self.weight_edit)
		self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)

		if not multi:
			self.index_edit.setText(idxs[0])
			self.name_edit.setText(names[0])
		else:
			self.index_edit.setText(', '.join(idxs))
			self.name_edit.setText(', '.join(names))
			self.index_edit.setEnabled(False)
			self.name_edit.setEnabled(False)
		self.layout = QVBoxLayout()
		self.layout.addLayout(self.form)
		self.layout.addWidget(self.buttons)
		self.setLayout(self.layout)
	
	def values(self):
		if self.multi:
			return self.weight_edit.text()
		else:
			return (self.index_edit.text(), self.name_edit.text(), self.weight_edit.text())