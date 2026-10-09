import sys
import logging

from .fmts import ColoredFormatter, IndentedFormatter
from core.utils import sanitize_path as p

def setup_logging(logfile=p('RSAP.log'), level=logging.INFO):
	logger = logging.getLogger()
	logger.setLevel(level)

	fmt = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
	console_handler = logging.StreamHandler(sys.stdout)
	if sys.stdout is not None and sys.stdout.isatty():
		console_handler.setFormatter(ColoredFormatter(fmt=fmt))
	else:
		console_handler.setFormatter(IndentedFormatter(fmt=fmt))

	file_handler = logging.FileHandler(logfile, encoding='utf-8', mode='a')
	file_handler.setFormatter(IndentedFormatter(fmt=fmt))

	logger.addHandler(console_handler)
	logger.addHandler(file_handler)
