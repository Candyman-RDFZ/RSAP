from core.config import ORG, NAME
from core.utils import sanitize_path as p
from core.settings import load as l

import json

LANG_MAP = {0: 'en-US', 1: 'zh-CN', 2: 'zh-TR'}
translation = {}

def upd_lang():
	global lang, translation
	lang = int(l('lang', 0))
	with open(p(LANG_MAP[lang] + '.json', True), 'r', encoding='utf-8') as file:
		translation = json.load(file)

upd_lang()

def get_lang():
	global lang
	return LANG_MAP[lang]

def tr(key, **kwargs):
	template = translation[key]
	return template.format(**kwargs) if kwargs else template
