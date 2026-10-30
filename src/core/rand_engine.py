from PySide6.QtCore import QTimer

import random
import logging

lgr = logging.getLogger(__name__)

class RandomEngine:
	def __init__(self, parent_wnd):
		lgr.info('Random engine initiated')
		self.parent_wnd = parent_wnd
		self.data = {
			'tot': 4,
			0: {
				'idx': '1',
				'name': 'Raina',
				'weight': 1
			},
			1: {
				'idx': '2',
				'name': 'ssssssssw',
				'weight': 1
			},
			2: {
				'idx': '3',
				'name': 'Jenny',
				'weight': 1
			},
			3: {
				'idx': '4',
				'name': 'Susan',
				'weight': 1
			}
		}
		
		self.tot = self.data['tot']
		self.tot_weight = 0
		for i in range(self.tot):
			self.tot_weight += self.data[i]['weight']

		self.pool = self.build_pool()

		self.stop_cnt = 20
		self.stop_timer = QTimer(self.parent_wnd)
		self.stop_timer.timeout.connect(self._timer_step)

		self.log_data()

	def reload_settings(self):
		
		lgr.info('Random engine settings reloaded')

	def log_data(self):
		self.data_str = f'Data:\nTotal: {self.tot}'
		for i in range(self.tot):
			cur_data = self.data[i]
			cur_chance = cur_data['weight'] / self.tot_weight * 100
			cur_str = f'No. {cur_data['idx']}; Name: {cur_data['name']}; Weight: {cur_data['weight']}; Chance: {cur_chance:.2f}%'
			self.data_str += '\n' + cur_str
		lgr.info(self.data_str)

	def build_pool(self) -> list:
		res = []
		for i in range(self.tot):
			cur_weight = self.data[i]['weight']
			for j in range(cur_weight):
				res.append(i)
		return res
	
	def _step(self) -> tuple:
		cur = random.choice(self.pool)
		idx = self.data[cur]['idx']
		name = self.data[cur]['name']
		lgr.info(f'Current person: No. {idx} ({name})')
		return (idx, name)

	def step(self, started=False):
		idx, name = self._step()
		self.parent_wnd.update_nn(idx, name)
		if started:
			self._stop_cnt -= 1
			lgr.info(f'Stop count is now {self._stop_cnt}')
			self.parent_wnd.start_btn.setText(f'Stop\n{self._stop_cnt} left')
			if self._stop_cnt == 0:
				self.stop()

	def _timer_step(self):
		self.step(True)

	def _start(self):
		self.stop_timer.start(100)
	
	def stop(self):
		self.stop_timer.stop()
		self._stop_cnt = self.stop_cnt
		self.parent_wnd.start_btn.setText('Start')
		self.parent_wnd.step_btn.setEnabled(True)
		lgr.info('Stopped')

	def start(self):
		self.parent_wnd.start_btn.setText(f'Stop\n{self.stop_cnt} left')
		self.parent_wnd.step_btn.setEnabled(False)
		self._stop_cnt = self.stop_cnt
		self._start()
	
	def toggle(self):
		if self.stop_timer.isActive():
			self.stop()
		else:
			self.start()
