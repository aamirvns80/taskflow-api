import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

LOG_LEVEL = logging.DEBUG if settings.app_env =="development" else logging.INFO

def configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    if getattr(root_logger,"_taskflow_configured", False):
        return
    root_logger._taskflow_configured = True


    base_dir = Path(__file__).resolve().parent.parent

    log_dir = base_dir/ "logs"
    log_dir.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10*1024*1024,
        backupCount=3,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    error_handler = RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=10*1024*1024,
        backupCount=3,
        encoding="utf-8"
    )

    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)

    root_logger._taskflow_configured = True












