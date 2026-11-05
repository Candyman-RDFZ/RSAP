'''Configuration file for RSAP'''
import sys
import pathlib
import platform

NAME = 'RSAP'
VERSION = '0.0pre'
FULL_NAME = NAME + ' version ' + VERSION
ORG = 'Candy_man'
ID = 'io.github.Candyman-RDFZ.RSAP'

PLATFORM = platform.system()

EXEC = getattr(sys, 'frozen', False)
ASSETS_ROOT = (pathlib.Path(sys._MEIPASS) if EXEC else pathlib.Path(__file__).parents[1]) / 'assets'
ROOT = pathlib.Path(sys.executable).parent if EXEC else pathlib.Path(__file__).parents[1]

DEFAULT_DATA = {'tot': 0, 'tot_weight': 0}