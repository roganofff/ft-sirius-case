import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config import settings

def setup_logger():
    logger = logging.getLogger("requests_api")
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(exist_ok=True, parents=True)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=1024 * 1024 * 5,  # 5MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()