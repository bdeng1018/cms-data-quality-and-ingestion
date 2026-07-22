"""
base_ingestion.py
Stage 02 — Base Ingestion Interface

Defines the abstract ingestion contract for all raw data sources.
POS and QIES ingestion classes implement this interface.

Branch 1 requires only:
- load_raw()
- validate_minimal_structure()
- describe()

No domain logic, cleaning, or alignment belongs here.
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseIngestionSource(ABC):
    """
    Abstract base class for raw ingestion sources.
    Provides the minimal interface required by Stage 02.
    """

    def __init__(self, raw_path: str):
        self.raw_path = raw_path

    @abstractmethod
    def load_raw(self) -> pd.DataFrame:
        """
        Load the raw file into a DataFrame.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def validate_minimal_structure(self, df: pd.DataFrame) -> None:
        """
        Ensure the DataFrame contains the minimal required columns.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def describe(self) -> dict:
        """
        Provide metadata about the ingestion source.
        Useful for diagnostics and pipeline runner.
        """
        pass
