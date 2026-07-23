"""
Stage 05 — Test: Output Isolation
================================================================================

This test verifies that Stage 05 writes output ONLY to the directory specified
via the --output argument.

Stage 05 must NOT:
- Write logs
- Write intermediate artifacts
- Write to Stage 01–04 directories
- Create stray files anywhere else

It must ONLY:
- Write pipeline_summary.json to the requested output path

This test uses a temporary directory to ensure full isolation.
"""

from unittest.mock import patch

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Test: Stage 05 writes ONLY to the specified output path
# ------------------------------------------------------------------------------
def test_stage05_output_isolated(tmp_path):
    """Stage 05 must not create any files outside the output directory."""

    # Prepare isolated output directory
    output_dir = tmp_path / "stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    # Mock config loader + orchestrator
    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch:

        mock_cfg.return_value = {"stage05": {"output_dir": str(output_dir)}}
        mock_orch.return_value = {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "success",
        }

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

    # Validate summary JSON exists
    assert output_path.exists()

    # Validate output directory contains ONLY the summary file
    files = list(output_dir.iterdir())
    assert files == [output_path], "Stage 05 created unexpected files"

    # Validate no stray files anywhere else in tmp_path
    stray = [p for p in tmp_path.rglob("*") if p.is_file() and p != output_path]
    assert stray == [], f"Unexpected files created: {stray}"
