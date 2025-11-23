import logging
from .config import settings


def configure_logging():
    level = getattr(logging, settings.CHIRON_LOG_LEVEL.upper(), logging.INFO)
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    ch.setFormatter(fmt)
    root.addHandler(ch)


def get_logger(name: str):
    return logging.getLogger(name)
