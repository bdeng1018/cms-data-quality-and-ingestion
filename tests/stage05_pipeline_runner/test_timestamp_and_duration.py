"""
Stage 05 — Test: Timestamp + Duration Fields
================================================================================

This test verifies that Stage 05 produces valid timestamp and duration fields in
pipeline_summary.json:

Required behavior:
- timestamp_start and timestamp_end must be ISO‑8601 strings
- timestamp_end must be >= timestamp_start
- duration_seconds must be a positive float
- duration_seconds must equal (end - start) within tolerance

All filesystem interactions use temporary directories for isolation.
"""

import datetime
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
# Test: Timestamp + duration fields are valid
# ------------------------------------------------------------------------------
def test_timestamp_and_duration(tmp_path):
    """Summary JSON must contain valid timestamps and duration."""

    stage_results = {
        "stage01": "success",
        "stage02": "success",
        "stage03": "success",
        "stage04": "success",
    }

    summary = _run_stage05(tmp_path, stage_results)

    # Extract fields
    ts_start = summary["timestamp_start"]
    ts_end = summary["timestamp_end"]
    duration = summary["duration_seconds"]

    # Validate ISO‑8601 format
    start_dt = datetime.datetime.fromisoformat(ts_start)
    end_dt = datetime.datetime.fromisoformat(ts_end)

    # Validate ordering
    assert end_dt >= start_dt, "timestamp_end must be >= timestamp_start"

    # Validate duration type
    assert isinstance(duration, float), "duration_seconds must be a float"

    # Validate duration correctness (within tolerance)
    delta = (end_dt - start_dt).total_seconds()
    assert abs(delta - duration) < 0.5, "duration_seconds mismatch"
