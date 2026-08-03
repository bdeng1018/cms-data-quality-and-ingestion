"""
Stage 05 — Test: CLI Argument Validation
================================================================================

This test verifies that run_pipeline.py handles CLI argument usage correctly
under the current pipeline contract.

Current behavior:
- Missing --config: pipeline uses default config path (no SystemExit)
- Missing --output: pipeline uses default output path (no SystemExit)
- Nonexistent config path: raises FileNotFoundError
- Valid arguments: pipeline runs and writes summary to the specified output path

All subprocess and filesystem interactions are mocked for isolation.
"""

from unittest.mock import patch

import pytest

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ==============================================================================
# Test: Missing --config argument
# ==============================================================================
def test_cli_missing_config():
    """
    Missing --config should NOT raise SystemExit under current behavior.
    Pipeline should fall back to default config path.
    """

    test_args = [
        "run_pipeline.py",
        "--output",
        "data/stage05_reports/pipeline_summary.json",
    ]

    with patch("sys.argv", test_args):
        # Should NOT raise SystemExit
        run_pipeline_main()


# ==============================================================================
# Test: Missing --output argument
# ==============================================================================
def test_cli_missing_output():
    """
    Missing --output should NOT raise SystemExit under current behavior.
    Pipeline should fall back to default output path.
    """

    test_args = [
        "run_pipeline.py",
        "--config",
        "configs/pipeline.yml",
    ]

    with patch("sys.argv", test_args):
        # Should NOT raise SystemExit
        run_pipeline_main()


# ==============================================================================
# Test: Nonexistent config path
# ==============================================================================
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


# ==============================================================================
# Test: Valid arguments allow execution
# ==============================================================================
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
