"""
Stage 05 — Test: Summary Structure
================================================================================

This test verifies that the Stage 05 summary JSON contains the correct structure:

Required top‑level fields:
- pipeline
- timestamp_start
- timestamp_end
- duration_seconds
- stages
- warnings

Required stage fields:
- stage01
- stage02
- stage03
- stage04

The test ensures:
- All fields exist
- All fields have correct types
- Stages map to string statuses
- Warnings is a list
"""

import json
from unittest.mock import patch

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Helper: run Stage 05 and return summary JSON
# ------------------------------------------------------------------------------
def _run_stage05(tmp_path, stage_results):
    """Run Stage 05 with mocked orchestrator + config loader."""

    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch:

        mock_cfg.return_value = {"stage05": {"output_dir": str(output_dir)}}
        mock_orch.return_value = stage_results

        test_args = [
            "run_pipeline.py",
            "--config",
            "configs/pipeline.yml",
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    with open(output_path, "r") as f:
        return json.load(f)


# ------------------------------------------------------------------------------
# Test: Summary structure is correct
# ------------------------------------------------------------------------------
def test_summary_structure(tmp_path):
    """Summary JSON must contain all required fields with correct types."""

    stage_results = {
        "stage01": "success",
        "stage02": "success",
        "stage03": "success",
        "stage04": "success",
    }

    summary = _run_stage05(tmp_path, stage_results)

    # Required top‑level fields
    required_fields = [
        "pipeline",
        "timestamp_start",
        "timestamp_end",
        "duration_seconds",
        "stages",
        "warnings",
    ]

    for field in required_fields:
        assert field in summary, f"Missing field: {field}"

    # Validate types
    assert isinstance(summary["pipeline"], str)
    assert isinstance(summary["timestamp_start"], str)
    assert isinstance(summary["timestamp_end"], str)
    assert isinstance(summary["duration_seconds"], float)
    assert isinstance(summary["warnings"], list)

    # Validate stages structure
    stages = summary["stages"]
    assert isinstance(stages, dict)

    for stage in ["stage01", "stage02", "stage03", "stage04"]:
        assert stage in stages, f"Missing stage: {stage}"
        assert isinstance(stages[stage], str), f"Stage value must be string: {stage}"
