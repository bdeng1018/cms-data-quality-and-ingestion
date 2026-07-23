"""
pos_ingestion.py
Stage 02 — Raw Ingestion for CMS POS Data
================================================================================
Loads raw POS data into a DataFrame, performs minimal shape checks, and logs
ingestion events.

Branch 1 guarantees ONLY:
- file exists
- file loads successfully (CSV or Parquet)
- DataFrame returned
- minimal required columns present

No cleaning, normalization, renaming, fallback logic, or domain validation
belongs here. All of that is handled in Stage 02 cleaning.
"""

import pandas as pd

from utils.file_io import ensure_exists, read_csv, read_parquet
from utils.logging_utils import get_logger

from .constants import POS_MIN_COLUMNS
from .exceptions import InvalidRawShapeError, MissingRawFileError


class PosIngestionSource:
    """
    Minimal ingestion class for CMS POS raw data.
    """

    def __init__(self, raw_path: str):
        self.raw_path = raw_path
        self.logger = get_logger("pos_ingestion")

    # ==========================================================================
    # Load raw POS file
    # ==========================================================================
    def load_raw(self) -> pd.DataFrame:
        """
        Load the raw POS file into a DataFrame.
        Supports CSV or Parquet based on file extension.
        Performs no cleaning or renaming.
        """
        self.logger.info(f"Loading POS raw file: {self.raw_path}")

        try:
            ensure_exists(self.raw_path)
        except FileNotFoundError:
            raise MissingRawFileError(self.raw_path)

        # Load raw file --------------------------------------------------------
        if self.raw_path.endswith(".csv"):
            df = read_csv(self.raw_path)
        elif self.raw_path.endswith(".parquet"):
            df = read_parquet(self.raw_path)
        else:
            raise ValueError(f"Unsupported POS file format: {self.raw_path}")

        # Add facility_id for Stage 03 + Stage 04 compatibility
        if "PRVDR_NUM" in df.columns:
            df["facility_id"] = df["PRVDR_NUM"]
        else:
            raise ValueError("POS dataset missing PRVDR_NUM; cannot derive facility_id")

        self.logger.info(f"Loaded POS file with shape: {df.shape}")
        return df

    # ==========================================================================
    # Minimal structure validation
    # ==========================================================================
    def validate_minimal_structure(self, df: pd.DataFrame) -> None:
        """
        Ensure the DataFrame contains the minimal required POS columns.
        No dtype checks, no normalization, no domain validation.
        """
        missing = [col for col in POS_MIN_COLUMNS if col not in df.columns]
        if missing:
            self.logger.error(f"Missing POS columns: {missing}")
            raise InvalidRawShapeError(missing)

        if df.shape[0] == 0:
            self.logger.error("POS dataset has zero rows.")
            raise InvalidRawShapeError(["<no rows>"])

        self.logger.info("POS minimal column validation passed.")

    # ==========================================================================
    # Metadata (diagnostics only)
    # ==========================================================================
    def describe(self) -> dict:
        """
        Provide metadata about the POS ingestion source.
        Useful for diagnostics and Stage 05 runner.
        """
        return {
            "source": "CMS POS",
            "path": self.raw_path,
            "required_columns": POS_MIN_COLUMNS,
        }
