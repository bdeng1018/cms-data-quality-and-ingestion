"""
Tests for Stage 03 Runner (run_stage03.py)

Validates:
    - schema loading
    - cleaned data loading
    - engine execution
    - artifact writing
    - logging behavior
    - error handling for missing files
"""

import json
from unittest.mock import patch

import pandas as pd
import pytest

import src.stage03_data_quality.run_quality as runner

# import src.stage03_data_quality.quality_writer as writer
# from pathlib import Path


@pytest.fixture(autouse=True)
def patch_paths(tmp_path, monkeypatch):
    """
    Redirect Stage 03 runner + writer paths to tmp_path.
    Prevents tests from touching real pipeline directories.
    """

    fake_intermediate = tmp_path / "stage03_intermediate"
    fake_intermediate.mkdir()

    # Patch writer default directory
    monkeypatch.setattr(
        "src.stage03_data_quality.quality_writer.DEFAULT_INTERMEDIATE_DIR",
        fake_intermediate,
    )

    # ⭐ Patch runner output directory (critical)
    monkeypatch.setattr(
        "src.stage03_data_quality.run_quality.OUTPUT_DIR",
        fake_intermediate,
    )

    # Fake schema + cleaned data paths
    fake_schema = tmp_path / "schema.json"
    fake_cleaned = tmp_path / "cleaned_data.csv"

    monkeypatch.setattr(runner, "SCHEMA_PATH", fake_schema)
    monkeypatch.setattr(runner, "CLEANED_DATA_PATH", fake_cleaned)

    # Create fake schema
    with fake_schema.open("w") as f:
        json.dump({"columns": {"facility_id": {}, "col1": {}, "col2": {}}}, f)

    # Create fake cleaned data
    df = pd.DataFrame(
        {
            "facility_id": ["A", "A", "B"],
            "col1": [1, 2, None],
            "col2": ["x", None, "z"],
        }
    )
    df.to_csv(fake_cleaned, index=False)

    return {
        "intermediate": fake_intermediate,
        "schema": fake_schema,
        "cleaned": fake_cleaned,
    }


# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------


def test_run_stage03_creates_artiIfacts(monkeypatch, tmp_path):
    """
    Validate that Stage 03 runner:
        - loads schema
        - loads cleaned data
        - runs quality engine
        - writes all three artifacts into OUTPUT_DIR
    """

    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps({"fields": ["facility_id", "city", "state"]}))

    cleaned_path = tmp_path / "cleaned.csv"
    cleaned_path.write_text("facility_id,city,state\n1,TestCity,CA\n")

    monkeypatch.setattr(runner, "SCHEMA_PATH", schema_path)
    monkeypatch.setattr(runner, "CLEANED_DATA_PATH", cleaned_path)

    output_dir = tmp_path / "stage03_intermediate"
    monkeypatch.setattr(runner, "OUTPUT_DIR", output_dir)

    runner.main()

    summary_path = output_dir / "quality_summary.json"
    facility_path = output_dir / "facility_metrics.csv"
    profiles_path = output_dir / "column_profiles.json"

    assert summary_path.exists()
    assert facility_path.exists()
    assert profiles_path.exists()

    summary = json.loads(summary_path.read_text())
    profiles = json.loads(profiles_path.read_text())
    df_facility = pd.read_csv(facility_path)

    assert isinstance(summary, dict)
    assert isinstance(profiles, dict)
    assert isinstance(df_facility, pd.DataFrame)


@patch("src.stage03_data_quality.run_quality.run_stage03_quality")
def test_run_stage03_calls_engine(mock_engine, patch_paths):
    """Ensure runner calls Stage 03 engine exactly once."""
    mock_engine.return_value = (
        {"total_rows": 3},
        pd.DataFrame({"facility_id": ["A"]}),
        {"col1": {"null_count": 1}},
    )

    runner.main()
    mock_engine.assert_called_once()


def test_run_stage03_missing_schema_raises(tmp_path, monkeypatch):
    """Runner should fail cleanly if schema.json is missing."""
    fake_schema = tmp_path / "missing_schema.json"
    fake_cleaned = tmp_path / "cleaned.csv"

    # Patch runner paths
    monkeypatch.setattr(runner, "SCHEMA_PATH", fake_schema)
    monkeypatch.setattr(runner, "CLEANED_DATA_PATH", fake_cleaned)

    with pytest.raises(FileNotFoundError):
        runner.main()


def test_run_stage03_missing_cleaned_data_raises(tmp_path, monkeypatch):
    """Runner should fail cleanly if cleaned_data.csv is missing."""
    fake_schema = tmp_path / "schema.json"
    fake_cleaned = tmp_path / "missing_cleaned.csv"

    # Create fake schema
    with fake_schema.open("w") as f:
        json.dump({"columns": {"facility_id": {}, "col1": {}, "col2": {}}}, f)

    # Patch runner paths
    monkeypatch.setattr(runner, "SCHEMA_PATH", fake_schema)
    monkeypatch.setattr(runner, "CLEANED_DATA_PATH", fake_cleaned)

    with pytest.raises(FileNotFoundError):
        runner.main()
