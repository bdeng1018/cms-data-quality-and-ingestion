"""
Stage 05 — Test: Stage 04 Artifact Validation
================================================================================

This test verifies that Stage 05 correctly validates Stage 04 processed outputs.

It ensures:
- validate_stage04_outputs() detects missing artifacts
- run_pipeline.py includes warnings when Stage 04 artifacts are incomplete
- run_pipeline.py includes no warnings when Stage 04 artifacts are complete

All filesystem interactions use temporary directories for isolation.
"""

import json
import os
from pathlib import Path
from unittest.mock import patch

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main
from src.stage05_pipeline_runner.run_pipeline import (
    validate_stage04_outputs,
)


# ------------------------------------------------------------------------------
# Test: validate_stage04_outputs detects missing files
# ------------------------------------------------------------------------------
def test_stage04_validation_missing(tmp_path):
    """Missing Stage 04 artifacts should be detected."""

    os.chdir(tmp_path)

    # Create only one artifact
    stage04 = tmp_path / "data/stage04_processed"
    stage04.mkdir(parents=True)
    (stage04 / "report_index.json").write_text("{}")

    # Patch working directory so validate_stage04_outputs sees tmp_path
    with patch("os.path.exists") as mock_exists:

        def fake_exists(path):
            return Path(path).exists()

        mock_exists.side_effect = fake_exists

        missing = validate_stage04_outputs()
        assert len(missing) == 2  # only inside tmp_path sandbox
        assert "facility_health.csv" in missing[0] or missing[1]
        assert "dataset_summary.json" in missing[0] or missing[1]


# ------------------------------------------------------------------------------
# Test: run_pipeline.py includes warnings when Stage 04 artifacts are missing
# ------------------------------------------------------------------------------
def test_stage05_summary_with_missing_stage04(tmp_path):
    """Summary JSON should include warnings when Stage 04 artifacts are missing."""

    # Prepare output directory
    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    # Mock config loader + orchestrator
    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch, patch(
        "src.stage05_pipeline_runner.run_pipeline.validate_stage04_outputs"
    ) as mock_validate:

        mock_cfg.return_value = {"stage05": {"output_dir": str(output_dir)}}
        mock_orch.return_value = {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "success",
        }

        mock_validate.return_value = [
            "data/stage04_processed/facility_health.csv",
            "data/stage04_processed/dataset_summary.json",
        ]

        # Simulate CLI args
        test_args = [
            "run_pipeline.py",
            "--config",
            "configs/pipeline.yml",
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    # Validate summary JSON
    with open(output_path, "r") as f:
        summary = json.load(f)

    assert summary["warnings"], "Expected warnings for missing Stage 04 artifacts"


# ------------------------------------------------------------------------------
# Test: run_pipeline.py includes NO warnings when Stage 04 artifacts are complete
# ------------------------------------------------------------------------------
def test_stage05_summary_no_warnings(tmp_path):
    """Summary JSON should contain no warnings when Stage 04 artifacts are complete."""

    # Prepare output directory
    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    # Mock config loader + orchestrator
    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch, patch(
        "src.stage05_pipeline_runner.run_pipeline.validate_stage04_outputs"
    ) as mock_validate:

        mock_cfg.return_value = {"stage05": {"output_dir": str(output_dir)}}
        mock_orch.return_value = {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "success",
        }

        mock_validate.return_value = []  # no missing artifacts

        # Simulate CLI args
        test_args = [
            "run_pipeline.py",
            "--config",
            "configs/pipeline.yml",
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    # Validate summary JSON
    with open(output_path, "r") as f:
        summary = json.load(f)

    assert summary["warnings"] == [], "Expected no warnings when Stage 04 is complete"
