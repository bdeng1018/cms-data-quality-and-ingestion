"""
Smoke test for QIES ingestion.
Ensures QIES ingestion loads a DataFrame and validates minimal columns.
"""

import pandas as pd

from stage02_raw_ingestion.constants import QIES_MIN_COLUMNS
from stage02_raw_ingestion.qies_ingestion import QiesIngestionSource


def test_qies_ingestion_smoke(tmp_path):
    # Create a minimal QIES CSV
    csv_path = tmp_path / "qies.csv"
    df = pd.DataFrame({col: ["x"] for col in QIES_MIN_COLUMNS})
    df.to_csv(csv_path, index=False)

    src = QiesIngestionSource(str(csv_path))
    loaded = src.load_raw()

    assert isinstance(loaded, pd.DataFrame)
    assert all(col in loaded.columns for col in QIES_MIN_COLUMNS)

    # Should not raise
    src.validate_minimal_structure(loaded)
