import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter


LOGGER = logging.getLogger(__name__)
LOGGERS = {}


class DuplicateFilter(logging.Filter):
    def filter(self, record):
        repeated_number_exists = getattr(self, "repeated_number", None)
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            if repeated_number_exists:
                LOGGER.warning(f"Last log repeated {self.repeated_number} times.")

            self.repeated_number = 0
            return True
        if repeated_number_exists:
            self.repeated_number += 1
        else:
            self.repeated_number = 1
        return False


class WrapperLogFormatter(ColoredFormatter):
    def formatTime(self, record, datefmt=None):  # noqa: N802
        return datetime.fromtimestamp(record.created).isoformat()


def get_logger(name):
    if LOGGERS.get(name):
        return LOGGERS.get(name)

    log_level = os.environ.get("OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL", "INFO")
    log_file = os.environ.get("OPENSHIFT_PYTHON_WRAPPER_LOG_FILE", "")
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid log level: {log_level}")

    logger_obj = logging.getLogger(name)
    log_formatter = WrapperLogFormatter(
        fmt="%(asctime)s %(name)s %(log_color)s%(levelname)s%(reset)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt=log_formatter)
    console_handler.addFilter(filter=DuplicateFilter())

    logger_obj.addHandler(hdlr=console_handler)
    logger_obj.setLevel(level=log_level)
    logger_obj.addFilter(filter=DuplicateFilter())

    if log_file:
        log_handler = RotatingFileHandler(
            filename=log_file, maxBytes=100 * 1024 * 1024, backupCount=20
        )
        log_handler.setFormatter(fmt=log_formatter)
        log_handler.setLevel(level=log_level)
        logger_obj.addHandler(hdlr=log_handler)

    logger_obj.propagate = False
    LOGGERS[name] = logger_obj
    return logger_obj
