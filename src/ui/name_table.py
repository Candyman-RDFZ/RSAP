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
		self.verticalHeader().setVisible(False)
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
		self.itemSelectionChanged.connect(self.update_edit_del)

		self.tot = 0
		self.tot_weight = 0

		self.update_edit_del()
	
	def update_edit_del(self):
		sel_rows = self.selectionModel().selectedRows()
		self.del_button.setEnabled(bool(sel_rows))
		self.edit_button.setEnabled(bool(sel_rows))

	def verify_data(self, row, index, name, weight, multi=False) -> bool:
		if not multi:
			for i in range(self.tot):
				if self.item(i, 0).text() == index and i != row:
					QMessageBox.critical(self.parent, 'Error - RSAP', f'The index ({index}) cannot be the same as No. {index} (Name: {self.item(i, 1).text()}; Weight: {self.item(i, 2).text()}).', buttons=QMessageBox.Ok)
					return False
		if weight == '':
			QMessageBox.critical(self.parent, 'Error - RSAP', 'The weight cannot be empty.', buttons=QMessageBox.Ok)
			return False
		if int(weight) < 0:
			QMessageBox.critical(self.parent, 'Error - RSAP', 'The weight cannot be smaller than 0.', buttons=QMessageBox.Ok)
			return False
		return True

	def upd_chances(self):
		for i in range(self.tot):
			if self.tot_weight:
				self.setItem(i, 3, QTableWidgetItem(str(f'{(int(self.item(i, 2).text()) / self.tot_weight * 100):.2f}%')))
			else:
				self.setItem(i, 3, QTableWidgetItem('/'))

	def add_row(self):
		dialog = AddDialog(self.parent, 1)
		if dialog.exec() != QDialog.Accepted:
			return None
		index, name, weight = dialog.values()
		weight = int(weight)
		
		if not self.verify_data(-1, index, name, weight, multi=True):
			return

		self.insertRow(self.tot)
		self.setItem(self.tot, 0, QTableWidgetItem(index))
		self.setItem(self.tot, 1, QTableWidgetItem(name))
		self.setItem(self.tot, 2, QTableWidgetItem(str(weight)))
		self.tot_weight += weight
		self.tot += 1
		self.upd_chances()
	
	def edit_row(self):
		sel_rows = self.selectionModel().selectedRows()
		if not sel_rows:
			return None

		rows = [cur.row() for cur in sel_rows]
		idxs = [self.item(row, 0).text() for row in rows]
		names = [self.item(row, 1).text() for row in rows]
		weights = [self.item(row, 2).text() for row in rows]
		multi = len(rows) != 1

		dialog = EditDialog(self.parent, idxs, names, 1 if multi else weights[0], multi)
		if dialog.exec() != QDialog.Accepted:
			return None
		values = dialog.values()

		if multi:
			if not self.verify_data(-1, None, None, int(values), True):
				return
			for row in rows:
				pre = self.item(row, 2).text()
				self.setItem(row, 2, QTableWidgetItem(str(values)))
				self.tot_weight -= int(pre) - int(values)
		else:
			row = rows[0]
			if not self.verify_data(row, values[0], values[1], values[2]):
				return
			self.setItem(row, 0, QTableWidgetItem(values[0]))
			self.setItem(row, 1, QTableWidgetItem(values[1]))
			pre = self.item(row, 2).text()
			if str(values[2]):
				self.setItem(row, 2, QTableWidgetItem(str(values[2])))
				self.tot_weight -= int(pre) - int(values[2])

		self.upd_chances()

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

	def get_value(self) -> dict:
		res = {'tot': self.tot, 'tot_weight': self.tot_weight}
		for i in range(self.tot):
			cur_data = {'idx': self.item(i, 0).text(), 'name': self.item(i, 1).text(), 'weight': int(self.item(i, 2).text())}
			res[i] = cur_data
		return res
	
	def set_value(self, data: dict):
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
				if self.tot_weight != 0:
					self.setItem(i, 3, QTableWidgetItem(f'{(weight / self.tot_weight * 100):.2f}%'))
				else:
					self.setItem(i, 3, QTableWidgetItem('/'))
		except Exception as e:
			print(e)
			dialog = QMessageBox.critical(self.parent, 'Error - RSAP', 'Cannot load data from settings.', buttons=QMessageBox.Ok)
			self.clearContents()
			self.setRowCount(0)
			self.tot = 0
			self.tot_weight = 0