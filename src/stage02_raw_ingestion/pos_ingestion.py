"""
pos_ingestion.py
Stage 02 — Raw Ingestion for CMS POS Data

Loads raw POS data into a DataFrame, performs minimal shape checks,
and logs ingestion events. No cleaning, normalization, or domain
validation belongs here (handled in later stages).
"""

import pandas as pd

from utils.file_io import ensure_exists, read_csv, read_parquet
from utils.logging_utils import get_logger

from .constants import POS_MIN_COLUMNS
from .exceptions import InvalidRawShapeError, MissingRawFileError


class PosIngestionSource:
    """
    Minimal ingestion class for CMS POS raw data.
    Branch 1 guarantees:
      - file loads successfully
      - DataFrame returned
      - minimal required columns present
    """

    def __init__(self, raw_path: str):
        self.raw_path = raw_path
        self.logger = get_logger("pos_ingestion")

    def load_raw(self) -> pd.DataFrame:
        """
        Load the raw POS file into a DataFrame.
        Supports CSV or Parquet based on file extension.
        """
        self.logger.info(f"Loading POS raw file: {self.raw_path}")

        try:
            ensure_exists(self.raw_path)
        except FileNotFoundError:
            raise MissingRawFileError(self.raw_path)

        if self.raw_path.endswith(".csv"):
            df = read_csv(self.raw_path)
        elif self.raw_path.endswith(".parquet"):
            df = read_parquet(self.raw_path)
        else:
            raise ValueError(f"Unsupported POS file format: {self.raw_path}")

        # Normalize CMS API → ingestion schema
        COLUMN_MAP = {
            "PRVDR_NUM": "ccn",
            "PRVDR_CTGRY_CD": "provider_type",
            "CITY_NAME": "city",
            "STATE_CD": "state",
            "ZIP_CD": "zip",
            "OWNERSHIP_CD": "ownership",
        }
        """Mapping from CMS API field names to ingestion schema names."""

        # Rename known fields
        df = df.rename(columns=COLUMN_MAP)

        # Address does not exist in API → use facility name as fallback
        if "address" not in df.columns:
            df["address"] = df.get("FAC_NAME", None)

        # Ensure all required ingestion columns exist
        required_cols = [
            "ccn",
            "provider_type",
            "address",
            "city",
            "state",
            "zip",
            "ownership",
        ]
        for col in required_cols:
            if col not in df.columns:
                df[col] = None

        self.logger.info(f"Loaded POS file with shape: {df.shape}")
        return df

    def validate_minimal_structure(self, df: pd.DataFrame) -> None:
        """
        Ensure the DataFrame contains the minimal required POS columns.
        """
        missing = [col for col in POS_MIN_COLUMNS if col not in df.columns]
        if missing:
            self.logger.error(f"Missing POS columns: {missing}")
            raise InvalidRawShapeError(missing)

        self.logger.info("POS minimal column validation passed.")

    def describe(self) -> dict:
        """
        Provide metadata about the POS ingestion source.
        Useful for diagnostics and Stage 5 runner.
        """
        return {
            "source": "CMS POS",
            "path": self.raw_path,
            "required_columns": POS_MIN_COLUMNS,
        }
