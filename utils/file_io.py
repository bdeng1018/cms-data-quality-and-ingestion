"""
utils/file_io.py
================================================================================
Shared file I/O utilities for the CMS POS/QIES ingestion pipeline.

Originally introduced in Stage 02 (raw ingestion), this module now supports
Stages 01–04 with safe, minimal, and deterministic helpers:

    - Existence checks
    - Directory creation
    - CSV / Parquet readers
    - DataFrame writers
    - Logging for pipeline observability

Design principles:
    - No domain logic
    - No cleaning or validation
    - No mutation of caller-owned objects
    - Safe for all pipeline stages (01–04)
"""

import logging
from pathlib import Path

import pandas as pd

# ==============================================================================
# Logging configuration
# ==============================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] utils.file_io: %(message)s")
    )
    logger.addHandler(handler)


# ==============================================================================
# Existence checks
# ==============================================================================
def ensure_exists(path: str | Path) -> None:
    path = Path(path)
    if not path.exists():
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")
    logger.info(f"Verified file exists: {path}")


# ==============================================================================
# Directory utilities
# ==============================================================================
def ensure_directory(path: str | Path) -> None:
    if not path:
        return

    path = Path(path)

    if not path.exists():
        logger.info(f"Creating directory: {path}")
        path.mkdir(parents=True, exist_ok=True)
    else:
        logger.info(f"Directory exists: {path}")


# ==============================================================================
# CSV / Parquet readers
# ==============================================================================
def read_csv(path: str | Path) -> pd.DataFrame:
    ensure_exists(path)
    logger.info(f"Reading CSV: {path}")
    return pd.read_csv(path)


def read_parquet(path: str | Path) -> pd.DataFrame:
    ensure_exists(path)
    logger.info(f"Reading Parquet: {path}")
    return pd.read_parquet(path)


# ==============================================================================
# DataFrame writer
# ==============================================================================
def write_df(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    ensure_directory(path.parent)

    logger.info(f"Writing DataFrame → {path}")
    df.to_csv(path, index=False)


# ==============================================================================
# Deterministic text I/O (added for diagnostics)
# ==============================================================================
def write_file(path: Path, content: str) -> None:
    """
    Deterministic UTF‑8 write with newline normalization.

    Diagnostics contract:
        - Normalize CRLF/CR → LF
        - Overwrite deterministically
        - UTF‑8 only
    """
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    path.write_text(normalized, encoding="utf-8")


def read_file(path: Path) -> str:
    """
    Deterministic UTF‑8 read with newline normalization.

    Diagnostics contract:
        - Normalize CRLF/CR → LF
        - Raise FileNotFoundError for missing files
        - UTF‑8 only
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    raw = path.read_text(encoding="utf-8")
    return raw.replace("\r\n", "\n").replace("\r", "\n")
