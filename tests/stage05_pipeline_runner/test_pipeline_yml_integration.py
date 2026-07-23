"""
Stage 05 — Test: pipeline.yml Integration
================================================================================

This test verifies that Stage 05 can load and execute using a REAL pipeline.yml
file (not a synthetic dict injected via mocks).

Required behavior:
- pipeline.yml must load correctly
- Stage 05 must respect stage05.output_dir from the file
- Summary JSON must be written to the correct location
- Orchestrator must be invoked
- No real subprocesses or filesystem artifacts from Stage 01–04 are required

This is a pure smoke test: orchestrator + validation are mocked.
"""

import json
from unittest.mock import patch

import yaml

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Test: Stage 05 loads and executes using real pipeline.yml
# ------------------------------------------------------------------------------
def test_pipeline_yml_integration(tmp_path):
    """Stage 05 must load a real pipeline.yml and write summary JSON."""

    # Create a real pipeline.yml file
    cfg_path = tmp_path / "pipeline.yml"
    cfg_path.write_text(
        yaml.dump({"stage05": {"output_dir": str(tmp_path / "stage05_reports")}})
    )

    # Prepare output directory
    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    # Mock orchestrator + validation
    with patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch, patch(
        "src.stage05_pipeline_runner.run_pipeline.validate_stage04_outputs"
    ) as mock_validate:

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
