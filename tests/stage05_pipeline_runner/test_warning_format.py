"""
Stage 05 — Test: Warning Format
================================================================================

This test verifies that Stage 05 formats warnings consistently in the final
pipeline_summary.json.

Required behavior:
- warnings must be a list
- each warning must be a string
- warnings must be human‑readable
- warnings must reference missing artifacts using deterministic paths
- warnings must be empty when no issues exist

All filesystem interactions use temporary directories for isolation.
"""

import json
from unittest.mock import patch

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Helper: run Stage 05 and return summary JSON
# ------------------------------------------------------------------------------
def _run_stage05(tmp_path, missing_artifacts):
    """Run Stage 05 with mocked orchestrator + config loader + validation."""

    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

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
        mock_validate.return_value = missing_artifacts

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
# Test: warnings list is empty when no issues exist
# ------------------------------------------------------------------------------
def test_warning_format_empty(tmp_path):
    """Warnings must be empty when Stage 04 validation passes."""

    summary = _run_stage05(tmp_path, missing_artifacts=[])

    assert summary["warnings"] == []
    assert isinstance(summary["warnings"], list)


# ------------------------------------------------------------------------------
# Test: warnings list contains readable strings
# ------------------------------------------------------------------------------
def test_warning_format_nonempty(tmp_path):
    """Warnings must be readable strings referencing missing artifacts."""

    missing = [
        "data/stage04_processed/facility_health.csv",
        "data/stage04_processed/dataset_summary.json",
    ]

    summary = _run_stage05(tmp_path, missing_artifacts=missing)

    warnings = summary["warnings"]

    # Must be a list
    assert isinstance(warnings, list)
    assert len(warnings) == 1  # Stage 05 collapses missing artifacts into one warning

    # Must be a readable string
    warning = warnings[0]
    assert isinstance(warning, str)

    # Must reference missing artifacts deterministically
    for artifact in missing:
        assert artifact in warning, f"Warning missing reference to {artifact}"

    # Must not contain structured objects
    assert "['" not in warning
    assert "{'" not in warning
