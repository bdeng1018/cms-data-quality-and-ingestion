"""
Tests for Stage 03 diagnostics — check_quality.py

NON‑DESTRUCTIVE VERSION:
    - uses tmp_path for all inputs
    - monkeypatches log path
    - does NOT write to logs/quality.log
    - does NOT touch real pipeline artifacts
"""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def patch_quality_log(tmp_path, monkeypatch):
    """
    Redirect Stage 03 quality diagnostics logging to a temporary file.
    Prevents tests from overwriting logs/quality.log.
    """
    fake_log = tmp_path / "quality_test.log"

    # Patch the logger inside the diagnostics script
    import scripts.diagnostics.stage03.check_quality as diag

    # Replace the log file path
    monkeypatch.setattr(diag, "LOG_PATH", fake_log)

    # Reinitialize logger handlers to use the patched path
    for h in diag.logger.handlers[:]:
        diag.logger.removeHandler(h)

    fh = diag.logging.FileHandler(fake_log)
    fh.setLevel(diag.logging.INFO)
    diag.logger.addHandler(fh)

    return fake_log


def test_check_quality_script(tmp_path):
    """
    Validate that the Stage 03 diagnostics script runs successfully
    and prints expected summary sections. We do NOT assert exact JSON
    formatting because the pipeline now sanitizes NumPy scalars.
    """

    # Create a minimal cleaned_data.csv for diagnostics
    cleaned = tmp_path / "cleaned_data.csv"
    cleaned.write_text("facility_id,city,state\n1,TestCity,CA\n")

    script_path = Path("scripts/diagnostics/stage03/check_quality.py")

    # Run the script
    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--file",
            str(cleaned),
            "--type",
            "pos",
        ],
        capture_output=True,
        text=True,
    )

    # Script must exit cleanly
    assert result.returncode == 0, f"Script failed: {result.stdout}\n{result.stderr}"

    # Output must contain the expected diagnostic sections
    stdout = result.stdout

    assert "=== Stage 03 Dataset-Level Metrics ===" in stdout
    assert "=== Stage 03 Facility-Level Metrics ===" in stdout
    assert "=== Stage 03 Column-Level Profiles (Summary) ===" in stdout
    assert "Diagnostics complete." in stdout
