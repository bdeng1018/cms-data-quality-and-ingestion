"""
Stage 02 — Raw Ingestion Package

Provides minimal ingestion classes, interfaces, and source loaders for CMS POS
and QIES raw data. This package defines the ingestion contract and
implements source-specific loaders used by later pipeline stages.

Branch 1 includes:
- BaseIngestionSource (interface)
- PosIngestionSource (POS loader)
- QiesIngestionSource (QIES loader)
- minimal column constants
- ingestion exceptions
"""

from .base_ingestion import BaseIngestionSource
from .constants import POS_MIN_COLUMNS, QIES_MIN_COLUMNS
from .exceptions import InvalidRawShapeError, MissingRawFileError
from .pos_ingestion import PosIngestionSource
from .qies_ingestion import QiesIngestionSource

__all__ = [
    "BaseIngestionSource",
    "PosIngestionSource",
    "QiesIngestionSource",
    "POS_MIN_COLUMNS",
    "QIES_MIN_COLUMNS",
    "MissingRawFileError",
    "InvalidRawShapeError",
]
