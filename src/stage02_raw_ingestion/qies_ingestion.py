"""
qies_ingestion.py
Stage 02 — Raw Ingestion for CMS QIES Data

Loads raw QIES data into a DataFrame, performs minimal shape checks,
and logs ingestion events. No cleaning, normalization, or domain
validation belongs here (handled in later stages).
"""

import pandas as pd

from utils.file_io import read_csv, read_parquet, ensure_exists
from utils.logging_utils import get_logger
from .constants import QIES_MIN_COLUMNS
from .exceptions import MissingRawFileError, InvalidRawShapeError


class QiesIngestionSource:
    """
    Minimal ingestion class for CMS QIES raw data.
    Branch 1 guarantees:
      - file loads successfully
      - DataFrame returned
      - minimal required columns present
    """

    def __init__(self, raw_path: str):
        self.raw_path = raw_path
        self.logger = get_logger("qies_ingestion")

    def load_raw(self) -> pd.DataFrame:
        """
        Load the raw QIES file into a DataFrame.
        Supports CSV or Parquet based on file extension.
        """
        self.logger.info(f"Loading QIES raw file: {self.raw_path}")

        try:
            ensure_exists(self.raw_path)
        except FileNotFoundError:
            raise MissingRawFileError(self.raw_path)

        if self.raw_path.endswith(".csv"):
            df = read_csv(self.raw_path)
        elif self.raw_path.endswith(".parquet"):
            df = read_parquet(self.raw_path)
        else:
            raise ValueError(f"Unsupported QIES file format: {self.raw_path}")

        self.logger.info(f"Loaded QIES file with shape: {df.shape}")
        return df

    def validate_minimal_structure(self, df: pd.DataFrame) -> None:
        """
        Ensure the DataFrame contains the minimal required QIES columns.
        """
        missing = [col for col in QIES_MIN_COLUMNS if col not in df.columns]
        if missing:
            self.logger.error(f"Missing QIES columns: {missing}")
            raise InvalidRawShapeError(missing)

        self.logger.info("QIES minimal column validation passed.")

    def describe(self) -> dict:
        """
        Provide metadata about the QIES ingestion source.
        Useful for diagnostics and Stage 5 runner.
        """
        return {
            "source": "CMS QIES",
            "path": self.raw_path,
            "required_columns": QIES_MIN_COLUMNS,
        }
