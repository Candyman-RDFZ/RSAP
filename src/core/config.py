'''Configuration file for RSAP'''
import sys
import pathlib
import platform

NAME = 'RSAP'
ORG = 'Candy_man'
VERSION = '2.5a'
ID = 'io.github.Candyman-RDFZ.RSAP'

PLATFORM = platform.system()

EXEC = getattr(sys, 'frozen', False)
ASSETS_ROOT = (pathlib.Path(sys._MEIPASS) if EXEC else pathlib.Path(__file__).parents[1]) / 'assets'
LANG_ROOT = (pathlib.Path(sys._MEIPASS) if EXEC else pathlib.Path(__file__).parents[1]) / 'lang'

DEFAULT_DATA = {'tot': 0, 'tot_weight': 0}
