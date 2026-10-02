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
DIR_ROOT = pathlib.Path(sys.executable).parent if EXEC else pathlib.Path(__file__).parents[1]
