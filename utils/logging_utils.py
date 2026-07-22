"""
logging_utils.py
Stage 02 — Raw Ingestion Logging Utilities

Provides lightweight logging helpers for POS/QIES ingestion.
Branch 1 only requires simple file-based logging with consistent
formatting. No domain-specific logging belongs here.
"""

import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "ingestion.log")


def get_logger(name: str) -> logging.Logger:
    """
    Create or retrieve a logger with consistent formatting.
    Logs are written to logs/ingestion.log for Stage 02.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers in interactive environments
    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
