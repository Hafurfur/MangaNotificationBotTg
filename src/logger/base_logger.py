import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

log = logging.getLogger('log')

Path.mkdir(Path(Path.cwd(), './logs/'), exist_ok=True)

rotation_handler = TimedRotatingFileHandler('./logs/log.log', utc=True, when='D')
stream_handler = logging.StreamHandler()

log.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.ERROR)

fmt_str = '[%(asctime)s] [%(name)s] [%(module)s] [%(levelname)s] -> %(message)s'
fmt_date = '%d-%m-%Y %H:%M:%S'
formatter_log = logging.Formatter(fmt_str, fmt_date)

rotation_handler.setFormatter(formatter_log)
stream_handler.setFormatter(formatter_log)

log.addHandler(rotation_handler)
log.addHandler(stream_handler)
