"""
Test Suite: Stage 04 Reporting Runner
===============================================================
Validates the orchestration layer of Stage 04 reporting.

The runner is responsible for:
    - locating Stage 03 artifacts
    - invoking the report engine
    - invoking the formatter
    - invoking the writer
    - producing Stage 04 processed artifacts

This suite ensures:
    - correct function calls
    - correct logging behavior
    - safe execution using temporary directories
    - no interaction with real pipeline data

All filesystem writes occur inside pytest's tmp_path sandbox.
"""

import json
import logging
from pathlib import Path

import pandas as pd

from src.stage04_reporting import run_reporting
from src.stage04_reporting.run_reporting import main as run_stage04

# ==============================================================================
# Configure test logger
# ==============================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(levelname)s] test_run_reporting: %(message)s")
    )
    logger.addHandler(handler)


# ==============================================================================
# Helper: Create synthetic Stage 03 artifacts
# ==============================================================================
def _create_stage03_artifacts(base_dir: Path):
    """
    Creates synthetic Stage 03 artifacts inside a temporary directory.
    These mimic real pipeline outputs but contain minimal test data.
    """

    stage03_dir = base_dir / "stage03_intermediate"
    stage03_dir.mkdir()

    # quality_summary.json
    (stage03_dir / "quality_summary.json").write_text(
        json.dumps(
            {
                "total_rows": 100,
                "column_count": 10,
                "facility_count": 100,
                "completeness_score": 0.25,
                "quality_score": 0.25,
            },
            indent=2,
        )
    )

    # column_profiles.json
    (stage03_dir / "column_profiles.json").write_text(
        json.dumps(
            {
                "colA": {
                    "completeness_score": 1.0,
                    "distinct_count": 10,
                    "inferred_dtype": "str",
                }
            },
            indent=2,
        )
    )

    # facility_metrics.csv
    df = pd.DataFrame(
        {
            "facility_id": ["A"],
            "completeness_score": [0.9],
        }
    )
    df.to_csv(stage03_dir / "facility_metrics.csv", index=False)

    return stage03_dir


# ==============================================================================
# Main Runner Test
# ==============================================================================
def test_run_reporting(tmp_path, monkeypatch):
    """
    Validate Stage 04 runner end‑to‑end using synthetic Stage 03 artifacts.

    Ensures:
        - runner loads Stage 03 artifacts
        - engine, formatter, writer are invoked
        - Stage 04 artifacts are written into tmp_path
        - no writes occur in real pipeline directories
    """

    logger.info("Running test_run_reporting...")

    # ----------------------------------------------------------------------
    # Create synthetic Stage 03 artifacts
    # ----------------------------------------------------------------------
    stage03_dir = _create_stage03_artifacts(tmp_path)

    # Patch runner paths to point to tmp_path
    monkeypatch.setattr(run_reporting, "STAGE03_DIR", stage03_dir)
    monkeypatch.setattr(
        run_reporting, "QUALITY_SUMMARY_PATH", stage03_dir / "quality_summary.json"
    )
    monkeypatch.setattr(
        run_reporting, "COLUMN_PROFILES_PATH", stage03_dir / "column_profiles.json"
    )
    monkeypatch.setattr(
        run_reporting, "FACILITY_METRICS_PATH", stage03_dir / "facility_metrics.csv"
    )

    # Patch output directory
    output_dir = tmp_path / "stage04_processed"
    monkeypatch.setattr(run_reporting, "DEFAULT_OUTPUT_DIR", output_dir)

    # ----------------------------------------------------------------------
    # Execute Stage 04 runner
    # ----------------------------------------------------------------------
    run_stage04()

    # ----------------------------------------------------------------------
    # Validate Stage 04 outputs
    # ----------------------------------------------------------------------
    assert output_dir.exists()

    expected_files = [
        "dataset_summary.json",
        "column_health.json",
        "sparse_columns.json",
        "facility_health.csv",
        "top_facilities.csv",
        "bottom_facilities.csv",
        "report_index.json",
    ]

    for filename in expected_files:
        path = output_dir / filename
        assert path.exists(), f"Missing expected Stage 04 artifact: {filename}"

    # Validate manifest loads correctly
    with (output_dir / "report_index.json").open("r") as f:
        manifest = json.load(f)

    assert "dataset_summary" in manifest
    assert "column_health" in manifest
    assert "facility_health" in manifest

    logger.info("✓ Stage 04 runner validated successfully.")


# --- Deterministic behavior tests for Stage 04 Reporting Runner ---


def test_run_stage04_is_deterministic(tmp_path, monkeypatch):
    """Running Stage 04 twice must produce identical artifacts."""
    stage03_dir = _create_stage03_artifacts(tmp_path)

    monkeypatch.setattr(run_reporting, "STAGE03_DIR", stage03_dir)
    monkeypatch.setattr(
        run_reporting, "QUALITY_SUMMARY_PATH", stage03_dir / "quality_summary.json"
    )
    monkeypatch.setattr(
        run_reporting, "COLUMN_PROFILES_PATH", stage03_dir / "column_profiles.json"
    )
    monkeypatch.setattr(
        run_reporting, "FACILITY_METRICS_PATH", stage03_dir / "facility_metrics.csv"
    )

    output_dir = tmp_path / "stage04_processed"
    monkeypatch.setattr(run_reporting, "DEFAULT_OUTPUT_DIR", output_dir)

    # First run
    run_stage04()
    ds1 = (output_dir / "dataset_summary.json").read_text()
    ch1 = (output_dir / "column_health.json").read_text()
    sc1 = (output_dir / "sparse_columns.json").read_text()
    fh1 = pd.read_csv(output_dir / "facility_health.csv")
    tf1 = pd.read_csv(output_dir / "top_facilities.csv")
    bf1 = pd.read_csv(output_dir / "bottom_facilities.csv")
    idx1 = (output_dir / "report_index.json").read_text()

    # Second run
    run_stage04()
    ds2 = (output_dir / "dataset_summary.json").read_text()
    ch2 = (output_dir / "column_health.json").read_text()
    sc2 = (output_dir / "sparse_columns.json").read_text()
    fh2 = pd.read_csv(output_dir / "facility_health.csv")
    tf2 = pd.read_csv(output_dir / "top_facilities.csv")
    bf2 = pd.read_csv(output_dir / "bottom_facilities.csv")
    idx2 = (output_dir / "report_index.json").read_text()

    # Deterministic JSON
    assert ds1 == ds2, "dataset_summary.json must be deterministic"
    assert ch1 == ch2, "column_health.json must be deterministic"
    assert sc1 == sc2, "sparse_columns.json must be deterministic"
    assert idx1 == idx2, "report_index.json must be deterministic"

    # Deterministic CSV
    assert fh1.equals(fh2), "facility_health.csv must be deterministic"
    assert tf1.equals(tf2), "top_facilities.csv must be deterministic"
    assert bf1.equals(bf2), "bottom_facilities.csv must be deterministic"


def test_stage04_manifest_key_order_is_deterministic(tmp_path, monkeypatch):
    """report_index.json keys must be sorted deterministically."""
    stage03_dir = _create_stage03_artifacts(tmp_path)

    monkeypatch.setattr(run_reporting, "STAGE03_DIR", stage03_dir)
    monkeypatch.setattr(
        run_reporting, "QUALITY_SUMMARY_PATH", stage03_dir / "quality_summary.json"
    )
    monkeypatch.setattr(
        run_reporting, "COLUMN_PROFILES_PATH", stage03_dir / "column_profiles.json"
    )
    monkeypatch.setattr(
        run_reporting, "FACILITY_METRICS_PATH", stage03_dir / "facility_metrics.csv"
    )

    output_dir = tmp_path / "stage04_processed"
    monkeypatch.setattr(run_reporting, "DEFAULT_OUTPUT_DIR", output_dir)

    run_stage04()

    manifest = json.loads((output_dir / "report_index.json").read_text())
    keys = list(manifest.keys())

    assert keys == sorted(
        keys
    ), "report_index.json keys must be sorted deterministically"


def test_stage04_csv_column_order_is_deterministic(tmp_path, monkeypatch):
    """All Stage 04 CSV artifacts must have deterministic column ordering."""
    stage03_dir = _create_stage03_artifacts(tmp_path)

    monkeypatch.setattr(run_reporting, "STAGE03_DIR", stage03_dir)
    monkeypatch.setattr(
        run_reporting, "QUALITY_SUMMARY_PATH", stage03_dir / "quality_summary.json"
    )
    monkeypatch.setattr(
        run_reporting, "COLUMN_PROFILES_PATH", stage03_dir / "column_profiles.json"
    )
    monkeypatch.setattr(
        run_reporting, "FACILITY_METRICS_PATH", stage03_dir / "facility_metrics.csv"
    )

    output_dir = tmp_path / "stage04_processed"
    monkeypatch.setattr(run_reporting, "DEFAULT_OUTPUT_DIR", output_dir)

    run_stage04()

    df_fac = pd.read_csv(output_dir / "facility_health.csv")
    df_top = pd.read_csv(output_dir / "top_facilities.csv")
    df_bottom = pd.read_csv(output_dir / "bottom_facilities.csv")

    assert list(df_fac.columns) == [
        "facility_id",
        "completeness_score",
        "health",
    ], "facility_health.csv must have deterministic column ordering"

    assert list(df_top.columns) == [
        "facility_id",
        "completeness_score",
    ], "top_facilities.csv must have deterministic column ordering"

    assert list(df_bottom.columns) == [
        "facility_id",
        "completeness_score",
    ], "bottom_facilities.csv must have deterministic column ordering"


def test_stage04_logging_is_deterministic(tmp_path, monkeypatch):
    """Stage 04 logging must be deterministic across repeated runs."""
    stage03_dir = _create_stage03_artifacts(tmp_path)

    monkeypatch.setattr(run_reporting, "STAGE03_DIR", stage03_dir)
    monkeypatch.setattr(
        run_reporting, "QUALITY_SUMMARY_PATH", stage03_dir / "quality_summary.json"
    )
    monkeypatch.setattr(
        run_reporting, "COLUMN_PROFILES_PATH", stage03_dir / "column_profiles.json"
    )
    monkeypatch.setattr(
        run_reporting, "FACILITY_METRICS_PATH", stage03_dir / "facility_metrics.csv"
    )

    output_dir = tmp_path / "stage04_processed"
    monkeypatch.setattr(run_reporting, "DEFAULT_OUTPUT_DIR", output_dir)

    log_path = output_dir / "stage04.log"
    monkeypatch.setattr(run_reporting, "LOG_PATH", log_path)

    run_stage04()
    log1 = log_path.read_text()

    run_stage04()
    log2 = log_path.read_text()

    assert log1 == log2, "Stage 04 log must be deterministic across repeated runs"
