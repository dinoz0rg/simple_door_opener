from logging.handlers import TimedRotatingFileHandler as TimedRotatingFileHandler
import logging
import os

LOG_WHEN = "W0"
LOG_INTERVAL = 1

log_location = f"{os.path.dirname(__file__)}/log"


def init_all_loggers(log_level, logger_type="normal"):
	if not os.path.exists(log_location):
		os.makedirs(log_location)

	formatter = logging.Formatter(
		u'%(asctime)s %(levelname)s %(message)s',
		datefmt="%Y-%m-%d %H:%M:%S"
	)
	cmd_logger = logging.getLogger()

	if logger_type == "timed":
		hdlr = TimedRotatingFileHandler(
			filename=f"{log_location}/logmain.log",
			encoding="utf-8",
			when=LOG_WHEN,
			interval=LOG_INTERVAL
		)
	else:
		hdlr = logging.FileHandler(
			filename=f"{log_location}/logmain.log",
			encoding="utf-8"
		)

	hdlr.setFormatter(formatter)
	cmd_logger.setLevel(log_level)  # INFO
	cmd_logger.addHandler(hdlr)
	hdlr2 = logging.StreamHandler()
	hdlr2.setFormatter(formatter)
	cmd_logger.addHandler(hdlr2)


def get_main_bot_logger():
	return logging.getLogger()  # return the default logger
