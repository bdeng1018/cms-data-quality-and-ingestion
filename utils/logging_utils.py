"""
logging_utils.py
Stage 02 — Raw Ingestion Logging Utilities

Provides lightweight logging helpers for POS/QIES ingestion.
Branch 1 only requires simple file-based logging with consistent
formatting. No domain-specific logging belongs here.
"""

import datetime
import json
import logging
from pathlib import Path


class JsonFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "timestamp": datetime.datetime.now().isoformat(),
        }
        return json.dumps({k: entry[k] for k in sorted(entry.keys())})


def get_logger(name: str, log_path: str | Path | None = None) -> logging.Logger:
    # Use the provided path EXACTLY
    if log_path is None:
        log_path = Path("logs") / f"{name}.log"
    else:
        log_path = Path(log_path)

    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Remove all handlers
    for h in list(logger.handlers):
        logger.removeHandler(h)

    # Attach JSON formatter
    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    logger.info("logger_initialized")

    return logger
