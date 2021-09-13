import logging

logger = logging.getLogger('log_analyzer')
logger.setLevel(logging.INFO)

log_format = logging.Formatter(
    '[%(asctime)s] %(levelname).1s %(message)s',
    datefmt='%Y.%m.%d %H:%M:%S'
)

handler = logging.StreamHandler()
handler.setFormatter(log_format)
logger.addHandler(handler)
