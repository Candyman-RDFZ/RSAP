from PySide6.QtCore import QSettings
from core.config import NAME, ORG, DEFAULT_DATA
from core.utils import get_window_dimension as g

import json
import logging
from random import randint
lgr = logging.getLogger(__name__)

settings = QSettings(ORG, NAME)

def save(key: str, value):
	global settings
	lgr.info(f'Saved settings {key} to {value}')
	settings.setValue(key, value)

def load(key: str, default):
	global settings
	if not settings.contains(key):
		lgr.info(f'Settings {key} does not yet exist. Setting to default value {default}')
		save(key, default)
	return settings.value(key)

def exp(filepath):
	l = load
	antirep_enabled = int(l('antirep_enabled', 1))
	antirep_num = int(l('antirep_num', int(l('data', DEFAULT_DATA)['tot']) // 2))
	ats_num = int(l('ats_num', 20))
	ats_time = int(l('ats_time', 100))
	data = dict(l('data', DEFAULT_DATA))
	initsz = l('initsz', g())
	initsz = (initsz.width(), initsz.height())
	seed_type = int(l('seed_type', 0))
	rand_seed = int(l('rand_seed', randint(0, int(1e15))))
	stay_on_top = int(l('stay_on_top', 1))
	wnd_behavior = int(l('wnd_behavior', 0))

	data = {
		'antirep_enabled': antirep_enabled,
		'antirep_num': antirep_num,
		'ats_num': ats_num,
		'ats_time': ats_time,
		'data': data,
		'seed_type': seed_type,
		'rand_seed': rand_seed,
		'wnd_behavior': wnd_behavior
	}

	with open(filepath, 'w') as file:
		json.dump(data, file, indent=4)

def imp(filepath):
	s = save
	data = {}
	with open(filepath, 'r') as file:
		data = json.load(file)
	s('antirep_enabled', data['antirep_enabled'])
	s('antirep_num', data['antirep_num'])
	s('ats_num', data['ats_num'])
	s('ats_time', data['ats_time'])
	s('data', data['data'])
	s('seed_type', data['seed_type'])
	s('rand_seed', data['rand_seed'])
	s('wnd_behavior', data['wnd_behavior'])