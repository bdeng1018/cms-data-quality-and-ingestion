"""
Stage 05 — Test: Orchestrator Execution Order
================================================================================

This test verifies that the Stage 05 orchestrator executes pipeline stages in the
correct deterministic order:

    Stage 01 → Stage 02 → Stage 03 → Stage 04

The test uses mocking to avoid running actual subprocess commands. It ensures:

- Correct ordering of subprocess calls
- Correct success/failure propagation
- Correct structure of the returned results dictionary
"""

from unittest.mock import call, patch

from src.stage05_pipeline_runner.orchestrator import run_all_stages


# ------------------------------------------------------------------------------
# Test: Successful execution sequence
# ------------------------------------------------------------------------------
def test_orchestrator_sequence_success():
    """Stages should run in correct order and return all 'success'."""

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = None  # simulate success

        config = {"stage05": {"output_dir": "data/stage05_reports"}}
        results = run_all_stages(config)

        # Validate results dictionary
        assert results == {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "success",
        }

        # Validate ordering of subprocess calls
        expected_calls = [
            call(
                ["python", "src/stage01_schema_definition/schema_loader.py"], check=True
            ),
            call(["python", "src/stage02_raw_ingestion/run_ingestion.py"], check=True),
            call(["python", "src/stage03_data_quality/run_quality.py"], check=True),
            call(["python", "src/stage04_reporting/run_reporting.py"], check=True),
        ]

        mock_run.assert_has_calls(expected_calls)


# ------------------------------------------------------------------------------
# Test: Fail-fast behavior
# ------------------------------------------------------------------------------
def test_orchestrator_sequence_fail_fast():
    """If Stage 01 fails, later stages must not run."""

    with patch("subprocess.run") as mock_run:
        # Stage 01 fails immediately
        mock_run.side_effect = Exception("Stage 01 failure")

        config = {"stage05": {"output_dir": "data/stage05_reports"}}
        results = run_all_stages(config)

        assert results == {
            "stage01": "failed",
            "stage02": "pending",
            "stage03": "pending",
            "stage04": "pending",
        }

        # Only Stage 01 should have been called
        mock_run.assert_called_once()
