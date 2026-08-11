"""
Smoke test for POS ingestion.
Ensures POS ingestion loads a DataFrame and validates minimal columns.
"""

import pandas as pd
import pytest

from src.stage02_raw_ingestion.constants import POS_MIN_COLUMNS
from src.stage02_raw_ingestion.pos_ingestion import PosIngestionSource


def test_pos_ingestion_smoke(tmp_path):
    # Create a minimal POS CSV
    csv_path = tmp_path / "pos.csv"
    df = pd.DataFrame({col: ["x"] for col in POS_MIN_COLUMNS})
    df.to_csv(csv_path, index=False)

    src = PosIngestionSource(str(csv_path))
    loaded = src.load_raw()

    assert isinstance(loaded, pd.DataFrame)
    assert all(col in loaded.columns for col in POS_MIN_COLUMNS)

    # Should not raise
    src.validate_minimal_structure(loaded)


# --- Deterministic ingestion tests for POS ingestion ---


def test_pos_ingestion_is_deterministic(tmp_path):
    """Repeated loads must produce identical DataFrames."""
    csv_path = tmp_path / "pos.csv"
    df = pd.DataFrame({col: ["x"] for col in POS_MIN_COLUMNS})
    df.to_csv(csv_path, index=False)

    src = PosIngestionSource(str(csv_path))

    loaded1 = src.load_raw()
    loaded2 = src.load_raw()

    # Deterministic row count
    assert len(loaded1) == len(loaded2), "Row count must be deterministic"

    # Deterministic column ordering
    assert list(loaded1.columns) == list(
        loaded2.columns
    ), "Column ordering must be deterministic"

    # Deterministic cell values
    assert loaded1.equals(loaded2), "Loaded DataFrame must be deterministic"


def test_pos_ingestion_metadata(tmp_path):
    """POS ingestion must attach deterministic metadata."""
    csv_path = tmp_path / "pos.csv"
    df = pd.DataFrame({col: ["x"] for col in POS_MIN_COLUMNS})
    df.to_csv(csv_path, index=False)

    src = PosIngestionSource(str(csv_path))
    loaded = src.load_raw()

    assert hasattr(
        loaded, "ingestion_metadata"
    ), "POS ingestion must attach ingestion_metadata"

    meta = loaded.ingestion_metadata

    # Required metadata fields
    required = {"source_path", "row_count", "columns"}
    missing = required - set(meta.keys())
    assert not missing, f"Missing ingestion metadata fields: {missing}"

    # Deterministic metadata values
    assert meta["source_path"] == str(csv_path), "source_path must be deterministic"
    assert meta["row_count"] == len(loaded), "row_count must match DataFrame"
    assert meta["columns"] == list(loaded.columns), "columns list must be deterministic"


def test_pos_ingestion_minimal_structure_is_deterministic(tmp_path):
    """validate_minimal_structure must behave deterministically."""
    csv_path = tmp_path / "pos.csv"
    df = pd.DataFrame({col: ["x"] for col in POS_MIN_COLUMNS})
    df.to_csv(csv_path, index=False)

    src = PosIngestionSource(str(csv_path))
    loaded = src.load_raw()

    # Should not raise
    src.validate_minimal_structure(loaded)
    src.validate_minimal_structure(loaded)  # repeat to ensure determinism


def test_pos_ingestion_rejects_missing_columns(tmp_path):
    """POS ingestion must reject CSVs missing required columns."""
    csv_path = tmp_path / "pos_bad.csv"
    df = pd.DataFrame({"id": ["x"]})  # missing many required columns
    df.to_csv(csv_path, index=False)

    src = PosIngestionSource(str(csv_path))
    loaded = src.load_raw()

    with pytest.raises(Exception):
        src.validate_minimal_structure(loaded)
