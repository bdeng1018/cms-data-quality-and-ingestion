"""
Stage 05 — Test: CLI Runner (run_pipeline.py)
================================================================================

This test verifies the behavior of the Stage 05 CLI runner:

- It loads configuration correctly
- It invokes the orchestrator
- It writes pipeline_summary.json
- It handles fail‑fast behavior correctly
- It does not execute real subprocess commands (mocked)

The test uses temporary directories and mocking to ensure isolation.
"""

import json
from unittest.mock import patch

import pytest

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Helper: run CLI with arguments
# ------------------------------------------------------------------------------
def _run_cli(tmpdir, orchestrator_return):
    """
    Execute run_pipeline.py with mocked orchestrator and config loader.

    Parameters
    ----------
    tmpdir : pathlib.Path
        Temporary directory for output file.
    orchestrator_return : dict
        Value returned by run_all_stages() mock.

    Returns
    -------
    dict
        Parsed pipeline_summary.json contents.
    """

    output_path = tmpdir / "pipeline_summary.json"

    # Mock config loader + orchestrator
    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch:

        mock_cfg.return_value = {"stage05": {"output_dir": str(tmpdir)}}
        mock_orch.return_value = orchestrator_return

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

    # Read summary JSON
    with open(output_path, "r") as f:
        return json.load(f)


# ------------------------------------------------------------------------------
# Test: Successful pipeline run
# ------------------------------------------------------------------------------
def test_run_pipeline_cli_success(tmp_path):
    """CLI runner should write summary JSON and report success."""

    orchestrator_return = {
        "stage01": "success",
        "stage02": "success",
        "stage03": "success",
        "stage04": "success",
    }

    summary = _run_cli(tmp_path, orchestrator_return)

    assert summary["pipeline"] == "cms-data-quality-and-ingestion"
    assert summary["stages"] == orchestrator_return
    assert "timestamp_start" in summary
    assert "timestamp_end" in summary
    assert "duration_seconds" in summary
    assert summary["warnings"] == []


# ------------------------------------------------------------------------------
# Test: Fail-fast behavior
# ------------------------------------------------------------------------------
def test_run_pipeline_cli_fail_fast(tmp_path):
    """If orchestrator raises an exception, summary should mark failure."""

    with patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch, patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg:

        mock_cfg.return_value = {"stage05": {"output_dir": str(tmp_path)}}
        mock_orch.side_effect = Exception("Stage 01 failure")

        output_path = tmp_path / "pipeline_summary.json"

        test_args = [
            "run_pipeline.py",
            "--config",
            "configs/pipeline.yml",
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            with pytest.raises(SystemExit):
                run_pipeline_main()

        # Validate summary JSON exists
        with open(output_path, "r") as f:
            summary = json.load(f)

        assert summary["stages"]["stage01"] == "failed"
        assert summary["stages"]["stage02"] == "skipped"
        assert summary["warnings"]
