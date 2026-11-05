from PySide6.QtCore import QTimer

from .settings import load as l

from random import Random, randint
import logging

lgr = logging.getLogger(__name__)

class RandomEngine:
	def __init__(self, parent_wnd):
		lgr.info('Random engine initiated')
		self.parent_wnd = parent_wnd
		self.seed_type = int(l('seed_type', 0))
		if not self.seed_type:
			self.rng = Random()
			lgr.info('Unseeded RNG')
		else:
			self.seed_val = int(l('rand_seed', randint(1, int(1e15))))
			self.rng = Random(self.seed_val)
			lgr.info(f'Seeded RNG with {self.seed_val}')

		self.data = dict(l('data', {'tot': 0, 'tot_weight': 0}))
		
		self.tot = self.data['tot']
		self.tot_weight = self.data['tot_weight']

		self.pool = self.build_pool()

		self.stop_cnt = int(l('ats_num', 20))
		self.stop_timer = QTimer(self.parent_wnd)
		self.stop_timer.timeout.connect(self._timer_step)

		self.antirep = True
		self.antirep_num = int(l('antirep_num', len(self.data) // 2))
		self.antirep_queue = []

		self.log_data()
		self.upd_btns()
	
	def upd_btns(self):
		self.parent_wnd.step_btn.setEnabled(bool(self.pool))
		self.parent_wnd.start_btn.setEnabled(bool(self.pool))

	def reload_settings(self):
		self.seed_type = int(l('seed_type', 0))
		if not self.seed_type:
			self.rng = Random()
			lgr.info('Unseeded RNG')
		else:
			self.seed_val = int(l('rand_seed', randint(1, int(1e15))))
			self.rng = Random(self.seed_val)
			lgr.info(f'Seeded RNG with {self.seed_val}')
		self.stop_cnt = int(l('ats_num', 20))
		self.antirep = int(l('antirep_enabled', 1))
		self.antirep_num = int(l('antirep_num', len(self.data) // 2))
		self.data = dict(l('data', {'tot': 0, 'tot_weight': 0}))
		self.tot = self.data['tot']
		self.tot_weight = self.data['tot_weight']
		self.pool = self.build_pool()
		self.antirep_queue = []

		self.upd_btns()
		lgr.info('Random engine settings reloaded')

	def log_data(self):
		self.data_str = f'Data:\nTotal: {self.tot}'
		if self.tot == 0 or self.tot_weight == 0: return
		for i in range(self.tot):
			cur_data = self.data[i]
			cur_chance = cur_data['weight'] / self.tot_weight * 100
			cur_str = f'No. {cur_data['idx']}; Name: {cur_data['name']}; Weight: {cur_data['weight']}; Chance: {cur_chance:.2f}%'
			self.data_str += '\n' + cur_str
		lgr.info(self.data_str)

	def build_pool(self) -> list:
		res = []
		if self.tot == 0:
			return []
		for i in range(self.tot):
			cur_weight = self.data[i]['weight']
			for j in range(cur_weight):
				res.append(i)
		return res
	
	def rem_from_pool(self, idx):
		pool_len = len(self.pool)
		self.pool = [self.pool[i] for i in range(pool_len) if self.pool[i] != idx]

	def add_to_pool(self, idx):
		weight = self.data[idx]['weight']
		for i in range(weight):
			self.pool.append(idx)

	def process_antirep(self, idx):
		self.antirep_queue.append(idx)
		lgr.info(f'Added item {idx} to the anti-repetition queue')
		self.rem_from_pool(idx)
		lgr.info(f'Removed item {idx} from the pool')
		lgr.info(f'Current pool: {self.pool}')
		if len(self.antirep_queue) == min(self.antirep_num, self.tot):
			popped = self.antirep_queue.pop(0)
			lgr.info(f'Anti-repetition queue full. Removed item {popped} from the anti-repetition queue')
			self.add_to_pool(popped)
			lgr.info(f'Re-added item {popped} to the pool')
			lgr.info(f'Current pool: {self.pool}')

	def _step(self) -> tuple:
		cur = self.rng.choice(self.pool)
		if self.antirep:
			self.process_antirep(cur)
		idx = self.data[cur]['idx']
		name = self.data[cur]['name']
		weight = self.data[cur]['weight']
		chance = self.data[cur]['weight'] / self.tot_weight * 100
		lgr.info(f'Current person: No. {idx} ({name})')
		return (idx, name, weight, chance)

	def step(self, started=False):
		idx, name, weight, chance = self._step()
		self.parent_wnd.update_nn(idx, name, weight, chance)
		if started:
			self._stop_cnt -= 1
			lgr.info(f'Stop count is now {self._stop_cnt}')
			self.parent_wnd.start_btn.setText(f'Stop\n{self._stop_cnt} left')
			if self._stop_cnt == 0:
				self.stop()

	def _timer_step(self):
		self.step(True)

	def _start(self):
		self.stop_timer.start(int(l('ats_time', 100)))
	
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
