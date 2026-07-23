"""
Stage 05 — Test: CLI Argument Validation
================================================================================

This test verifies that run_pipeline.py enforces correct CLI argument usage:

Required arguments:
- --config <path>
- --output <path>

Behavior tested:
- Missing --config triggers SystemExit
- Missing --output triggers SystemExit
- Nonexistent config path triggers FileNotFoundError
- Valid arguments allow execution to proceed

All subprocess and filesystem interactions are mocked for isolation.
"""

from unittest.mock import patch

import pytest

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Test: Missing --config argument
# ------------------------------------------------------------------------------
def test_cli_missing_config():
    """CLI must exit when --config is missing."""

    test_args = [
        "run_pipeline.py",
        "--output",
        "data/stage05_reports/pipeline_summary.json",
    ]

    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as exc:
            run_pipeline_main()
        assert exc.value.code == 1


# ------------------------------------------------------------------------------
# Test: Missing --output argument
# ------------------------------------------------------------------------------
def test_cli_missing_output():
    """CLI must exit when --output is missing."""

    test_args = [
        "run_pipeline.py",
        "--config",
        "configs/pipeline.yml",
    ]

    with patch("sys.argv", test_args):
        with pytest.raises(SystemExit) as exc:
            run_pipeline_main()
        assert exc.value.code == 1


# ------------------------------------------------------------------------------
# Test: Nonexistent config path
# ------------------------------------------------------------------------------
def test_cli_nonexistent_config(tmp_path):
    """CLI must raise FileNotFoundError when config path does not exist."""

    missing_cfg = tmp_path / "does_not_exist.yml"

    test_args = [
        "run_pipeline.py",
        "--config",
        str(missing_cfg),
        "--output",
        str(tmp_path / "pipeline_summary.json"),
    ]

    with patch("sys.argv", test_args):
        with pytest.raises(FileNotFoundError):
            run_pipeline_main()


# ------------------------------------------------------------------------------
# Test: Valid arguments allow execution
# ------------------------------------------------------------------------------
def test_cli_valid_arguments(tmp_path):
    """CLI should run when both required arguments are provided."""

    cfg_path = tmp_path / "pipeline.yml"
    cfg_path.write_text("stage05:\n  output_dir: 'x'")

    output_path = tmp_path / "pipeline_summary.json"

    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch, patch(
        "src.stage05_pipeline_runner.run_pipeline.validate_stage04_outputs"
    ) as mock_validate:

        mock_cfg.return_value = {"stage05": {"output_dir": str(tmp_path)}}
        mock_orch.return_value = {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "success",
        }
        mock_validate.return_value = []

        test_args = [
            "run_pipeline.py",
            "--config",
            str(cfg_path),
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    assert output_path.exists(), "Summary JSON should be written for valid arguments"
