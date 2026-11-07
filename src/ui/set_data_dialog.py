"""A custom dialog when the user clickes the add/edit buttons on the start page."""

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout, QHBoxLayout, QSpinBox, QLayout, QPushButton

from core.utils import get_dlg_dimension as g
from core.translator import tr

class AddDialog(QDialog):
	def __init__(self, parent, default_weight):
		super().__init__(parent)
		self.setWindowTitle(tr('nametb_addp') + ' - RSAP')
		self.setFixedSize(g())
		self.index_edit = QLineEdit()
		self.name_edit = QLineEdit()
		self.weight_edit = QSpinBox()
		self.weight_edit.setValue(int(default_weight))
		self.weight_edit.setMinimum(0)
		
		self.form = QFormLayout()
		self.form.addRow(tr('nametb_idx') + ': ', self.index_edit)
		self.form.addRow(tr('nametb_name') + ': ', self.name_edit)
		self.form.addRow(tr('nametb_wei') + ': ', self.weight_edit)

		self.button_box = QDialogButtonBox()
		self.ok_btn = self.button_box.addButton(tr('stgwnd_ok'), QDialogButtonBox.ButtonRole.AcceptRole)
		self.cancel_btn = self.button_box.addButton(tr('stgwnd_cancel'), QDialogButtonBox.ButtonRole.RejectRole)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)
		
		self.layout = QVBoxLayout()
		self.layout.addLayout(self.form)
		self.layout.addWidget(self.button_box)
		self.setLayout(self.layout)

		self.layout.setSizeConstraint(QLayout.SetFixedSize)
	
	def values(self) -> tuple:
		return (self.index_edit.text(), self.name_edit.text(), self.weight_edit.value())

class EditDialog(QDialog):
	def __init__(self, parent, idxs, names, default_weight, multi: bool):
		super().__init__(parent)
		self.multi = multi
		self.setWindowTitle(tr('nametb_editp') + ' - RSAP')
		self.setFixedSize(g())
		self.index_edit = QLineEdit()
		self.name_edit = QLineEdit()
		self.weight_edit = QSpinBox()
		self.weight_edit.setMinimum(0)
		if not multi:
			self.weight_edit.setValue(int(default_weight))
		
		self.form = QFormLayout()
		self.form.addRow(tr('nametb_idx') + ': ', self.index_edit)
		self.form.addRow(tr('nametb_name') + ': ', self.name_edit)
		self.form.addRow(tr('nametb_wei') + ': ', self.weight_edit)

		self.button_box = QDialogButtonBox()
		self.ok_btn = self.button_box.addButton(tr('stgwnd_ok'), QDialogButtonBox.ButtonRole.AcceptRole)
		self.cancel_btn = self.button_box.addButton(tr('stgwnd_cancel'), QDialogButtonBox.ButtonRole.RejectRole)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)

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
		self.layout.addWidget(self.button_box)
		self.setLayout(self.layout)

		self.layout.setSizeConstraint(QLayout.SetFixedSize)
	
	def values(self):
		if self.multi:
			return self.weight_edit.value()
		else:
			return (self.index_edit.text(), self.name_edit.text(), self.weight_edit.value())