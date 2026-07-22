"""
Tests for Stage 03 diagnostics — check_quality.py

This suite validates:
    - the diagnostics script executes without errors
    - a log file is created
    - quality checks run end-to-end on a temporary CSV

This test mirrors Stage 01 and Stage 02 diagnostic patterns.
"""

import subprocess
import sys
from pathlib import Path
import pandas as pd


def test_check_quality_script(tmp_path):
    """
    End-to-end test for the Stage 03 diagnostics script.

    Steps:
        1. Create a temporary CSV file
        2. Run the diagnostics script via subprocess
        3. Ensure no errors occur
        4. Ensure the quality log file is created
    """

    # 1. Create a temporary CSV file
    temp_csv = tmp_path / "temp_pos.csv"
    df = pd.DataFrame(
        {
            "ccn": [100, 200, 200],
            "provider_type": ["A", "B", "B"],
            "address": ["x", "y", "z"],
            "city": ["LA", "NY", "SF"],
            "state": ["CA", "NY", "CA"],
            "zip": ["90001", "10001", "94102"],
            "ownership": ["Non-profit", "Gov", "Non-profit"],
        }
    )
    df.to_csv(temp_csv, index=False)

    # 2. Run diagnostics script
    script_path = Path("scripts/diagnostics/stage03/check_quality.py")

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--file",
            str(temp_csv),
            "--type",
            "pos",
        ],
        capture_output=True,
        text=True,
    )

    # 3. Ensure script ran successfully
    assert result.returncode == 0, f"Script failed: {result.stderr}"

    # 4. Ensure log file was created
    log_path = Path("logs/quality.log")
    assert log_path.exists(), "Quality log file was not created."
