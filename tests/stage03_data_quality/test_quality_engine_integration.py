"""
Tests for Stage 03 Quality Engine Integration

Validates:
    - dataset-level metrics shape
    - facility-level metrics shape
    - column-level profiles shape
    - engine return structure (new architecture)
    - error handling for missing facility_id
"""

import pandas as pd
import pytest

import src.stage03_data_quality.quality_engine as engine
from src.stage03_data_quality.quality_engine import run_stage03_quality
from src.stage03_data_quality.quality_writer import (
    write_column_profiles,
    write_facility_metrics,
    write_quality_summary,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "facility_id": ["A", "A", "B"],
            "col1": [1, 2, None],
            "col2": ["x", None, "z"],
        }
    )


@pytest.fixture
def sample_schema():
    return {
        "columns": {
            "facility_id": {"required": True},
            "col1": {"dtype": "int"},
            "col2": {"dtype": "string"},
        }
    }


def test_compute_dataset_metrics_shape(sample_df, sample_schema):
    summary = engine.compute_dataset_metrics(sample_df, sample_schema)

    assert "total_rows" in summary
    assert "column_count" in summary
    assert "missingness_summary" in summary
    assert "quality_score" in summary

    assert summary["total_rows"] == 3
    assert summary["column_count"] == 3


def test_compute_facility_metrics_shape(sample_df):
    df_facility = engine.compute_facility_metrics(sample_df)

    assert "facility_id" in df_facility.columns
    assert "row_count" in df_facility.columns
    assert "missingness_rate" in df_facility.columns
    assert len(df_facility) == 2


def test_compute_facility_metrics_missing_facility_id():
    df = pd.DataFrame({"col1": [1, 2, 3]})

    with pytest.raises(ValueError):
        engine.compute_facility_metrics(df)


def test_compute_column_profiles_shape(sample_df):
    profiles = engine.compute_column_profiles(sample_df)

    assert "col1" in profiles
    assert "col2" in profiles
    assert profiles["col1"]["null_count"] == 1
    assert profiles["col2"]["distinct_count"] == 2


def test_run_stage03_quality_writes_artifacts_to_tmp(tmp_path):
    """
    Permanent fix:
    Tests write Stage 03 artifacts into tmp_path, never into the real pipeline
    directory. This prevents pytest leftovers from polluting data/stage03_intermediate/.
    """

    # ----------------------------------------------------------------------
    # 1. Create minimal schema + cleaned dataset
    # ----------------------------------------------------------------------
    schema = {"fields": ["facility_id", "city", "state"]}

    cleaned_path = tmp_path / "cleaned.csv"
    cleaned_path.write_text("facility_id,city,state\n1,TestCity,CA\n")

    df = pd.read_csv(cleaned_path)

    # ----------------------------------------------------------------------
    # 2. Run Stage 03 quality engine
    # ----------------------------------------------------------------------
    summary_dict, df_facility, column_profiles = run_stage03_quality(df, schema)

    # ----------------------------------------------------------------------
    # 3. Write artifacts into tmp_path (NOT pipeline directory)
    # ----------------------------------------------------------------------
    write_quality_summary(summary_dict, base_dir=tmp_path)
    write_facility_metrics(df_facility, base_dir=tmp_path)
    write_column_profiles(column_profiles, base_dir=tmp_path)

    # ----------------------------------------------------------------------
    # 4. Assertions on tmp_path artifacts
    # ----------------------------------------------------------------------
    summary_file = tmp_path / "quality_summary.json"
    facility_file = tmp_path / "facility_metrics.csv"
    profiles_file = tmp_path / "column_profiles.json"

    assert summary_file.exists()
    assert facility_file.exists()
    assert profiles_file.exists()

    # Validate summary JSON structure
    summary_loaded = summary_file.read_text()
    assert "total_rows" in summary_loaded
    assert "column_count" in summary_loaded

    # Validate facility metrics CSV
    df_loaded = pd.read_csv(facility_file)
    assert "facility_id" in df_loaded.columns
    assert len(df_loaded) >= 1

    # Validate column profiles JSON
    profiles_loaded = profiles_file.read_text()
    assert "facility_id" in profiles_loaded
    assert "null_count" in profiles_loaded
    assert "distinct_count" in profiles_loaded
