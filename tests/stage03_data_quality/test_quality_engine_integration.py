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


# --- Deterministic behavior tests for Stage 03 Quality Engine Integration ---


def test_dataset_metrics_are_deterministic(sample_df, sample_schema):
    """Repeated calls to compute_dataset_metrics must be deterministic."""
    m1 = engine.compute_dataset_metrics(sample_df, sample_schema)
    m2 = engine.compute_dataset_metrics(sample_df, sample_schema)

    assert m1 == m2, "Dataset metrics must be deterministic across repeated runs"


def test_facility_metrics_are_deterministic(sample_df):
    """Facility metrics must be deterministic across repeated runs."""
    f1 = engine.compute_facility_metrics(sample_df)
    f2 = engine.compute_facility_metrics(sample_df)

    assert f1.equals(f2), "Facility metrics DataFrame must be deterministic"


def test_facility_metrics_column_order_is_deterministic(sample_df):
    """Facility metrics must have deterministic column ordering."""
    df_facility = engine.compute_facility_metrics(sample_df)

    expected_order = [
        "facility_id",
        "row_count",
        "missingness_rate",
        "quality_score",
    ]

    assert (
        list(df_facility.columns) == expected_order
    ), "Facility metrics column ordering must be deterministic"


def test_column_profiles_are_deterministic(sample_df):
    """Column profiles must be deterministic across repeated runs."""
    p1 = engine.compute_column_profiles(sample_df)
    p2 = engine.compute_column_profiles(sample_df)

    assert p1 == p2, "Column profiles must be deterministic across repeated runs"


def test_column_profiles_key_order_is_deterministic(sample_df):
    """Column profile keys must be sorted deterministically."""
    profiles = engine.compute_column_profiles(sample_df)

    for col, prof in profiles.items():
        assert list(prof.keys()) == sorted(
            prof.keys()
        ), f"Column profile keys for {col} must be sorted deterministically"


def test_run_stage03_quality_is_deterministic(tmp_path):
    """run_stage03_quality must produce deterministic outputs."""
    schema = {"fields": ["facility_id", "city", "state"]}

    cleaned_path = tmp_path / "cleaned.csv"
    cleaned_path.write_text("facility_id,city,state\n1,TestCity,CA\n")

    df = pd.read_csv(cleaned_path)

    out1 = run_stage03_quality(df, schema)
    out2 = run_stage03_quality(df, schema)

    summary1, facility1, profiles1 = out1
    summary2, facility2, profiles2 = out2

    assert summary1 == summary2, "Summary dict must be deterministic"
    assert facility1.equals(facility2), "Facility metrics must be deterministic"
    assert profiles1 == profiles2, "Column profiles must be deterministic"


def test_written_artifacts_are_deterministic(tmp_path):
    """Artifacts written by Stage 03 must be deterministic."""
    schema = {"fields": ["facility_id", "city", "state"]}

    cleaned_path = tmp_path / "cleaned.csv"
    cleaned_path.write_text("facility_id,city,state\n1,TestCity,CA\n")

    df = pd.read_csv(cleaned_path)

    summary_dict, df_facility, column_profiles = run_stage03_quality(df, schema)

    # Write artifacts twice
    write_quality_summary(summary_dict, base_dir=tmp_path)
    write_facility_metrics(df_facility, base_dir=tmp_path)
    write_column_profiles(column_profiles, base_dir=tmp_path)

    write_quality_summary(summary_dict, base_dir=tmp_path)
    write_facility_metrics(df_facility, base_dir=tmp_path)
    write_column_profiles(column_profiles, base_dir=tmp_path)

    summary_file = tmp_path / "quality_summary.json"
    facility_file = tmp_path / "facility_metrics.csv"
    profiles_file = tmp_path / "column_profiles.json"

    # Deterministic summary JSON
    s1 = summary_file.read_text()
    s2 = summary_file.read_text()
    assert s1 == s2, "quality_summary.json must be deterministic"

    # Deterministic facility metrics CSV
    f1 = pd.read_csv(facility_file)
    f2 = pd.read_csv(facility_file)
    assert f1.equals(f2), "facility_metrics.csv must be deterministic"

    # Deterministic column profiles JSON
    p1 = profiles_file.read_text()
    p2 = profiles_file.read_text()
    assert p1 == p2, "column_profiles.json must be deterministic"
