"""
Stage 05 — Test: Summary Written Exactly Once
================================================================================

This test verifies that Stage 05 writes pipeline_summary.json exactly once:

Required behavior:
- Summary file is created a single time
- No temporary or partial summary files are created
- Summary is not overwritten multiple times
- Only one write operation occurs during run_pipeline.py

All filesystem interactions use temporary directories for isolation.
"""

from unittest.mock import mock_open, patch

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Helper: run Stage 05 with mocked orchestrator + config loader
# ------------------------------------------------------------------------------
def _run_stage05(tmp_path):
    """Run Stage 05 with mocks and return output path."""

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
        mock_validate.return_value = []

        test_args = [
            "run_pipeline.py",
            "--config",
            "configs/pipeline.yml",
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    return output_path


# ------------------------------------------------------------------------------
# Test: Summary file is written exactly once
# ------------------------------------------------------------------------------
def test_summary_written_once(tmp_path):
    """Summary JSON must be written exactly once."""

    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    # Track file writes
    m = mock_open()

    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch, patch(
        "src.stage05_pipeline_runner.run_pipeline.validate_stage04_outputs"
    ) as mock_validate, patch(
        "builtins.open", m
    ):

        mock_cfg.return_value = {"stage05": {"output_dir": str(output_dir)}}
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
            "configs/pipeline.yml",
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    # Validate exactly one write call
    write_calls = [c for c in m.mock_calls if c[0] == "().write"]

    assert len(write_calls) == 1, f"Expected exactly one write, got {len(write_calls)}"

    # Validate file exists
    assert output_path.exists(), "Summary JSON must exist after Stage 05 run"

    # Validate no stray files
    files = list(output_dir.iterdir())
    assert files == [output_path], "Unexpected extra files created in output directory"
