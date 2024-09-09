import logging
import os

from logging.handlers import RotatingFileHandler
from settings import BASE_DIR


def setup_logging(name):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)

    if os.path.exists(BASE_DIR / 'logs') is False:
        os.mkdir(BASE_DIR / 'logs')

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    stream.setLevel(logging.DEBUG)

    debug_handler = RotatingFileHandler(os.path.join(BASE_DIR, 'logs', 'debug.log'))
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    info_handler = RotatingFileHandler(os.path.join(BASE_DIR, 'logs', 'info.log'))
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(os.path.join(BASE_DIR, 'logs', 'error.log'))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(stream)