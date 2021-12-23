import logging
import os

from colorlog import ColoredFormatter


def get_logger(name):
    log_level = os.environ.get("OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL", "INFO")
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid log level: {log_level}")

    logger_obj = logging.getLogger(name)
    log_formatter = ColoredFormatter(
        fmt="%(name)s %(asctime)s %(log_color)s%(levelname) s%(reset)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
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
    logger_obj.addHandler(hdlr=console_handler)
    logger_obj.addHandler(hdlr=console_handler)
    logger_obj.setLevel(level=log_level)
    logger_obj.propagate = False
    return logger_obj
