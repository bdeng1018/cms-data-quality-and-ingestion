"""
Stage 02 — Raw Ingestion Package
================================================================================

This package implements Stage 02 of the CMS Data Quality & Ingestion Pipeline:
the deterministic raw‑ingestion layer responsible for loading POS/QIES source
files, verifying minimal structure, emitting ingestion metadata, and integrating
with the v1.1.0 C++ mechanization layer.

Stage 02 responsibilities include:

- Loading raw POS/QIES files (CSV or Parquet)
- Verifying minimal required columns defined in `constants.py`
- Emitting ingestion logs and structural metadata
- Running deterministic C++ row counting (v1.1.0)
- Propagating mechanization exit codes to Stage 05
- Providing ingestion artifacts for Stage 03 quality checks

Modules
-------
base_ingestion.py
    Defines the BaseIngestionSource interface and shared ingestion behavior.

pos_ingestion.py
    Implements POS ingestion, minimal column validation, and mechanization hooks.

qies_ingestion.py
    Implements QIES ingestion, minimal column validation, and mechanization hooks.

constants.py
    Defines minimal POS/QIES column requirements.

exceptions.py
    Provides deterministic ingestion error types.

run_ingestion.py
    CLI entrypoint for manual ingestion testing.

Notes
-----
Stage 02 performs no cleaning, normalization, CCN validation, or alignment.
It provides the raw ingestion skeleton for Branch 1 and integrates with the
deterministic C++ row counter introduced in v1.1.0.

All ingestion outputs are reproducible across local, Docker, Compose, Kubernetes,
Helm, and CI/CD environments.
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
