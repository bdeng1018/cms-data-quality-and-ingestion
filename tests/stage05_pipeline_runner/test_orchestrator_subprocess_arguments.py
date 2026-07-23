"""
Stage 05 — Test: Subprocess Argument Contract
================================================================================

This test verifies that the Stage 05 orchestrator invokes each stage using the
EXACT deterministic subprocess arguments defined in the pipeline contract.

Required behavior:
- Stage 01 command must match schema_loader.py
- Stage 02 command must match run_ingestion.py
- Stage 03 command must match run_quality.py
- Stage 04 command must match run_reporting.py
- No additional flags, env vars, or arguments may be added
- Ordering must be preserved

This is a pure smoke test: subprocess.run is fully mocked.
"""

from unittest.mock import call, patch

from src.stage05_pipeline_runner.orchestrator import run_all_stages


# ------------------------------------------------------------------------------
# Test: subprocess arguments match exact contract
# ------------------------------------------------------------------------------
def test_orchestrator_subprocess_arguments():
    """Orchestrator must call each stage with exact deterministic arguments."""

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = None  # simulate success

        config = {"stage05": {"output_dir": "data/stage05_reports"}}
        run_all_stages(config)

        expected_calls = [
            call(
                ["python", "src/stage01_schema_definition/schema_loader.py"], check=True
            ),
            call(["python", "src/stage02_raw_ingestion/run_ingestion.py"], check=True),
            call(["python", "src/stage03_data_quality/run_quality.py"], check=True),
            call(["python", "src/stage04_reporting/run_reporting.py"], check=True),
        ]

        mock_run.assert_has_calls(expected_calls)
        assert mock_run.call_count == 4
