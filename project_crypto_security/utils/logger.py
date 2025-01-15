import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_level: str = 'INFO') -> logging.Logger:
    """Configure and return a logger instance"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(console_handler)

    # File handler
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        f'{log_dir}/{name}.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(file_handler)

    return logger
