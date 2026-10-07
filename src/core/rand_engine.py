import random
import logging

lgr = logging.getLogger(__name__)

class RandomEngine:
	def __init__(self, parent_wnd):
		lgr.info('Random engine initiated')
		self.parent_wnd = parent_wnd
		self.data = {
			'tot': 4,
			'0': {
				'idx': '1',
				'name': '冯心仪',
				'weight': 1
			},
			'1': {
				'idx': '02',
				'name': '胡熙冉',
				'weight': 1
			},
			'2': {
				'idx': '03',
				'name': '李景仪',
				'weight': 1
			},
			'3': {
				'idx': '04',
				'name': '齐泽雨',
				'weight': 1
			}
		}
		
		self.tot = self.data['tot']

		self.pool = self.build_pool()
		lgr.info(f'Pool:\n{self.pool}')
	
	def build_pool(self) -> list:
		res = []
		for i in range(self.tot):
			cur_weight = self.data[str(i)]['weight']
			for j in range(cur_weight):
				res.append(i)
		return res
	
	def step(self):
		cur = random.choice(self.pool)
		idx = self.data[str(cur)]['idx']
		name = self.data[str(cur)]['name']
		lgr.info(f'Current person: No. {idx} ({name})')
		self.parent_wnd.update_nn(idx, name)

	
