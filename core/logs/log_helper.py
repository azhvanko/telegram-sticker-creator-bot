import logging
import os

from core.config import LOGS_DIR


_DEFAULT_FORMATTER = logging.Formatter(
    fmt='[%(levelname)-8s] [%(filename)-18s] [%(asctime)s] [%(message)s]',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def _get_file_handler(log_file: str, formatter: logging.Formatter,
                      level: int) -> logging.FileHandler:
    file_handler = logging.FileHandler(
        filename=os.path.join(LOGS_DIR, log_file),
        mode='a',
        encoding='utf-8',
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    return file_handler


def get_logger(*, log_file: str = 'log.log',
               formatter: logging.Formatter = _DEFAULT_FORMATTER) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

    log_file = os.path.join(LOGS_DIR, log_file)
    logger.addHandler(_get_file_handler(log_file, formatter, logging.WARNING))

    return logger
