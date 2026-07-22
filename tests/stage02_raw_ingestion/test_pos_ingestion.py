"""
Smoke test for POS ingestion.
Ensures POS ingestion loads a DataFrame and validates minimal columns.
"""

import pandas as pd

from stage02_raw_ingestion.constants import POS_MIN_COLUMNS
from stage02_raw_ingestion.pos_ingestion import PosIngestionSource


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
