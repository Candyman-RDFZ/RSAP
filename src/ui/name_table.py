"""A custom QWidget for displaying the references entered by the user.
Supports adding, editing, deletion, and drag-and-drop order altering.
"""

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QAbstractItemView, QDialog, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QMessageBox

from .set_data_dialog import AddDialog, EditDialog

class NameTableWidget(QTableWidget):
	def __init__(self, add_button: QPushButton, edit_button: QPushButton, del_button: QPushButton, parent=None):
		super().__init__(parent)
		self.parent = parent

		self.add_button = add_button
		self.edit_button = edit_button
		self.del_button = del_button

		self.setColumnCount(4)
		self.setHorizontalHeaderLabels(['Index', 'Name', 'Weight', 'Chance'])
		self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.setDragEnabled(True)
		self.setAcceptDrops(True)
		self.setDropIndicatorShown(True)
		self.setDragDropMode(QAbstractItemView.DragDrop)
		self.setDefaultDropAction(Qt.MoveAction)
		self.dragged_row = -1
		
		self.add_button.clicked.connect(self.add_row)
		self.edit_button.clicked.connect(self.edit_row)
		self.del_button.clicked.connect(self.del_row)

		self.tot = 0
		self.tot_weight = 0
		self.data = {}
	
	def verify_data(self, index, name, weight) -> bool:
		for i in range(self.tot):
			if self.data[i]['idx'] == index:
				QMessageBox.critical(self.parent, 'Error - RSAP', f'The index ({index}) cannot be the same as No. {index} (Name: {self.data[i]['name']}; Weight: {self.data[i]['weight']}).', buttons=QMessageBox.Ok)
				return False
		if weight < 0:
			QMessageBox.critical(self.parent, 'Error - RSAP', 'The weight cannot be smaller than 0.', buttons=QMessageBox.Ok)
			return False
		return True

	def upd_chances(self):
		for i in range(self.tot):
			self.setItem(i, 3, QTableWidgetItem(str(f'{(self.data[i]['weight'] / self.tot_weight * 100):.2f}%')))

	def add_row(self):
		dialog = AddDialog(self.parent, False)
		if dialog.exec() != QDialog.Accepted:
			return None
		index, name, weight = dialog.values()
		weight = int(weight)
		
		if not self.verify_data(index, name, weight):
			return

		self.insertRow(self.tot)
		self.setItem(self.tot, 0, QTableWidgetItem(index))
		self.setItem(self.tot, 1, QTableWidgetItem(name))
		self.setItem(self.tot, 2, QTableWidgetItem(str(weight)))
		self.data[self.tot] = {'idx': index, 'name': name, 'weight': weight}
		self.tot_weight += weight
		self.tot += 1
		self.upd_chances()
	
	def edit_row(self):
		sel_rows = self.selectionModel().selectedRows()
		if not sel_rows:
			return None
		row = sel_rows[0].row()
		ref_name = self.item(row, 0).text()
		doi_num = self.item(row, 1).text()
		
		dialog = AddEditDialog(self.parent, True, ref_name, doi_num)
		if dialog.exec() != QDialog.Accepted:
			return None
		name, doi = dialog.values()
		self.setItem(row, 0, QTableWidgetItem(name))
		self.setItem(row, 1, QTableWidgetItem(doi))

	def del_row(self, row=None):
		sel_rows = self.selectionModel().selectedRows()
		if not sel_rows:
			return None
		rows = [cur.row() for cur in sel_rows]
		rows.sort(reverse=True)
		for row in rows:
			weight = self.item(row, 2).text()
			self.removeRow(row)
			self.tot -= 1
			self.tot_weight -= int(weight)

		self.upd_chances()

	def startDrag(self, supported_actions):
		sel_rows = self.selectionModel().selectedRows()
		if not sel_rows:
			return None
		self.dragged_row = sel_rows[0].row()
		mime_data = QMimeData()
		drag = QDrag(self)
		drag.setMimeData(mime_data)
		drag.exec(Qt.MoveAction)
		self.dragged_row = -1
	
	def dragEnterEvent(self, event):
		if event.source() is self:
			event.acceptProposedAction()
		else:
			event.ignore()
	
	def dragMoveEvent(self, event):
		if event.source() is self:
			event.acceptProposedAction()
		else:
			event.ignore()
	
	def dropEvent(self, event):
		if event.source() is not self:
			event.ignore()
			return None
		if self.dragged_row < 0:
			event.ignore()
			return None
		pos = event.position().toPoint()
		target = self.rowAt(pos.y())
		if target < 0:
			event.ignore()
			return None
		if target == self.dragged_row:
			event.acceptProposedAction()
			return
		self.swap_rows(self.dragged_row, target)
		self.selectRow(target)
		event.acceptProposedAction()
	
	def swap_rows(self, row1, row2):
		for col in range(2):
			item1 = self.item(row1, col)
			item2 = self.item(row2, col)
			item1 = item1.clone() if item1 else None
			item2 = item2.clone() if item2 else None
			self.setItem(row1, col, item2)
			self.setItem(row2, col, item1)

	def get_value(self):
		if self.tot == 0:
			return None
		res = {}
		res['has_data'] = False
		res['count'] = self.tot
		for row in range(self.tot):
			ref_name = self.item(row, 0).text()
			doi_num = self.item(row, 1).text()
			res[str(row + 1)] = {'ref_name': ref_name, 'doi_num': doi_num}
		return res
	
	def set_value(self, data):
		try:
			self.tot = int(data['tot'])
			self.tot_weight = int(data['tot_weight'])
			self.setRowCount(self.tot)
			for i in range(self.tot):
				cur_dict = data[i]
				index = cur_dict['idx']
				name = cur_dict['name']
				weight = cur_dict['weight']
				self.setItem(i, 0, QTableWidgetItem(index))
				self.setItem(i, 1, QTableWidgetItem(name))
				self.setItem(i, 2, QTableWidgetItem(str(weight)))
				self.setItem(i, 3, QTableWidgetItem(f'{(weight / self.tot_weight * 100):.2f}%'))
				self.data = data
		except Exception as e:
			print(e)
			dialog = QMessageBox.critical(self.parent, 'Error - RSAP', 'The draft file cannot be loaded. The file is probably corrupted.', buttons=QMessageBox.Ok)

			# We reset the table. Refilling support will be added later. 
			self.clearContents()
			self.setRowCount(0)
			self.tot = 0