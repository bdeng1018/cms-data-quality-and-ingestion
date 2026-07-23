"""
Stage 05 — Test: Orchestrator Error Handling
================================================================================

This test verifies that the Stage 05 orchestrator handles subprocess errors
correctly:

- _run_stage() returns "failed" when subprocess.run raises an exception
- run_all_stages() propagates failure deterministically
- Later stages are NOT executed after a failure
- Error messages printed by _run_stage() do not break test execution

All subprocess calls are mocked to avoid running real pipeline stages.
"""

from unittest.mock import patch

from src.stage05_pipeline_runner.orchestrator import (
    _run_stage,
    run_all_stages,
)


# ------------------------------------------------------------------------------
# Test: _run_stage returns "failed" on subprocess error
# ------------------------------------------------------------------------------
def test_run_stage_failure():
    """_run_stage() should return 'failed' when subprocess.run raises."""

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("boom")

        result = _run_stage(["python", "fake.py"], "stage01")
        assert result == "failed"


# ------------------------------------------------------------------------------
# Test: run_all_stages stops after Stage 01 failure
# ------------------------------------------------------------------------------
def test_orchestrator_fail_stage01():
    """If Stage 01 fails, no later stages should run."""

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


# ------------------------------------------------------------------------------
# Test: run_all_stages stops after Stage 02 failure
# ------------------------------------------------------------------------------
def test_orchestrator_fail_stage02():
    """If Stage 02 fails, Stage 03 and Stage 04 must not run."""

    with patch("subprocess.run") as mock_run:
        # Stage 01 succeeds, Stage 02 fails
        mock_run.side_effect = [
            None,  # Stage 01 success
            Exception("Stage 02 fail"),  # Stage 02 failure
        ]

        config = {"stage05": {"output_dir": "data/stage05_reports"}}
        results = run_all_stages(config)

        assert results == {
            "stage01": "success",
            "stage02": "failed",
            "stage03": "pending",
            "stage04": "pending",
        }

        # Only Stage 01 and Stage 02 should have been called
        assert mock_run.call_count == 2


# ------------------------------------------------------------------------------
# Test: run_all_stages stops after Stage 03 failure
# ------------------------------------------------------------------------------
def test_orchestrator_fail_stage03():
    """If Stage 03 fails, Stage 04 must not run."""

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            None,  # Stage 01 success
            None,  # Stage 02 success
            Exception("Stage 03 fail"),  # Stage 03 failure
        ]

        config = {"stage05": {"output_dir": "data/stage05_reports"}}
        results = run_all_stages(config)

        assert results == {
            "stage01": "success",
            "stage02": "success",
            "stage03": "failed",
            "stage04": "pending",
        }

        assert mock_run.call_count == 3


# ------------------------------------------------------------------------------
# Test: run_all_stages handles Stage 04 failure
# ------------------------------------------------------------------------------
def test_orchestrator_fail_stage04():
    """If Stage 04 fails, earlier stages should still be marked success."""

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            None,  # Stage 01 success
            None,  # Stage 02 success
            None,  # Stage 03 success
            Exception("Stage 04 fail"),  # Stage 04 failure
        ]

        config = {"stage05": {"output_dir": "data/stage05_reports"}}
        results = run_all_stages(config)

        assert results == {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "failed",
        }

        assert mock_run.call_count == 4
