"""
Stage 05 — Test: End‑to‑End Dry‑Run (Fully Mocked)
================================================================================

This test performs a full end‑to‑end dry‑run of Stage 05:

- CLI argument parsing
- Config loading
- Stage 04 validation
- Orchestrator execution
- Summary JSON writing
- Timestamp + duration fields
- Warning formatting
- Output isolation

All heavy operations (subprocess, filesystem reads, validation) are mocked.
This test ensures the entire Stage 05 control‑plane works as a single unit.
"""

import datetime
import json
from unittest.mock import patch

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Test: Full end‑to‑end dry‑run
# ------------------------------------------------------------------------------
def test_end_to_end_dry_run(tmp_path):
    """Stage 05 must run end‑to‑end with all components mocked."""

    # Create real pipeline.yml
    cfg_path = tmp_path / "pipeline.yml"
    cfg_path.write_text(
        "stage05:\n  output_dir: '{}'\n".format(tmp_path / "stage05_reports")
    )

    # Prepare output directory
    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    # Mock orchestrator + validation + timestamps
    with patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch, patch(
        "src.stage05_pipeline_runner.run_pipeline.validate_stage04_outputs"
    ) as mock_validate, patch(
        "src.stage05_pipeline_runner.run_pipeline.datetime"
    ) as mock_dt:

        # Deterministic timestamps
        mock_dt.datetime.now.side_effect = [
            datetime.datetime(2025, 1, 1, 12, 0, 0),
            datetime.datetime(2025, 1, 1, 12, 0, 1),
        ]

        mock_orch.return_value = {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "success",
        }
        mock_validate.return_value = []

        # Simulate CLI args
        test_args = [
            "run_pipeline.py",
            "--config",
            str(cfg_path),
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    # Validate summary JSON exists
    assert output_path.exists(), "Summary JSON must be written"

    # Validate summary JSON structure
    with open(output_path, "r") as f:
        summary = json.load(f)

    assert summary["pipeline"] == "cms-data-quality-and-ingestion"
    assert summary["stages"]["stage01"] == "success"
    assert summary["warnings"] == []

    # Validate timestamps
    assert summary["timestamp_start"] == "2025-01-01T12:00:00"
    assert summary["timestamp_end"] == "2025-01-01T12:00:01"
    assert summary["duration_seconds"] == 1.0

    # Validate no stray files
    files = list(output_dir.iterdir())
    assert files == [output_path], "Unexpected files created in output directory"
