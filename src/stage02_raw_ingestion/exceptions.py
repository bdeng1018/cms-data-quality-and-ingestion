"""
Stage 02 — Raw Ingestion Exceptions
================================================================================
Lightweight exception classes used by POS/QIES ingestion modules.

Branch 1 design:
    - Minimal error signaling only
    - No domain-specific validation
    - No cleaning or schema logic
"""

from typing import List


class MissingRawFileError(FileNotFoundError):
    """
    Raised when a required raw POS/QIES file is not found.
    """

    def __init__(self, path: str):
        super().__init__(f"Raw ingestion file not found: {path}")


class InvalidRawShapeError(ValueError):
    """
    Raised when a raw file loads but does not contain the minimal
    required columns for Stage 02 ingestion.
    """

    def __init__(self, missing_columns: List[str]):
        msg = (
            "Raw ingestion file is missing required columns: "
            f"{', '.join(missing_columns)}"
        )
        super().__init__(msg)
