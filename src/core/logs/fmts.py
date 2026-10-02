import logging

from core.utils import sanitize_path as p

class IndentedFormatter(logging.Formatter):
	def format(self, record):
		raw_msg = record.getMessage()
		msg = super().format(record)
		pre = msg.split(raw_msg, 1)[0]
		indent = ' ' * len(pre)

		return msg.replace('\n', '\n' + indent)

class ColoredFormatter(logging.Formatter):
	COLORS = {
		logging.INFO: '\033[94m',
		logging.WARNING: '\033[33m',
		logging.ERROR: '\033[31m'
	}
	RESET = '\033[0m'

	def format(self, record):
		levelname = record.levelname
		raw_msg = record.getMessage()
		msg = super().format(record)
		pre = msg.split(raw_msg, 1)[0]

		color = self.COLORS.get(record.levelno)
		if color:
			record.levelname = f'{color}{levelname}{self.RESET}'
		try:
			msg = super().format(record)
			indent = ' ' * len(pre)
			return msg.replace('\n', '\n' + indent)
		finally:
			record.levelname = levelname
