"""
Stage 05 — Orchestrator
================================================================================

Executes Stages 01–04 in deterministic order:

    Stage 01 → Stage 02 → Stage 03 → Stage 04

Uses module-mode execution so Python resolves imports correctly inside Docker.
"""

import subprocess


# ==============================================================================
# Helper: run a stage command
# ==============================================================================
def _run_stage(cmd, stage_name):
    """
    Execute a stage command using subprocess.

    Parameters
    ----------
    cmd : list[str]
        The command to execute, e.g. ["python", "-m", "src.stage02_raw_ingestion.run_ingestion"]
    stage_name : str
        Name of the stage ("stage01", "stage02", ...)

    Returns
    -------
    str
        "success" or "failed"
    """
    try:
        subprocess.run(cmd, check=True)
        return "success"
    except Exception as e:
        print(f"[Stage05] ERROR: {stage_name} failed: {e}")
        return "failed"


# ==============================================================================
# Orchestrator: run all stages in correct order
# ==============================================================================
def run_all_stages(config):
    """
    Execute Stage 01 → Stage 02 → Stage 03 → Stage 04 in deterministic order.

    Returns a dict describing success/failure for each stage.
    """

    results = {
        "stage01": "pending",
        "stage02": "pending",
        "stage03": "pending",
        "stage04": "pending",
    }

    # --------------------------------------------------------------------------
    # Stage 01 — Schema Definition
    # --------------------------------------------------------------------------
    cmd_stage01 = ["python", "-m", "src.stage01_schema_definition.schema_loader"]
    results["stage01"] = _run_stage(cmd_stage01, "stage01")

    if results["stage01"] != "success":
        return results

    # --------------------------------------------------------------------------
    # Stage 02 — Raw Ingestion + Cleaning
    # --------------------------------------------------------------------------
    cmd_stage02 = ["python", "-m", "src.stage02_raw_ingestion.run_ingestion"]
    results["stage02"] = _run_stage(cmd_stage02, "stage02")

    if results["stage02"] != "success":
        return results

    # --------------------------------------------------------------------------
    # Stage 03 — Data Quality
    # --------------------------------------------------------------------------
    cmd_stage03 = ["python", "-m", "src.stage03_data_quality.run_quality"]
    results["stage03"] = _run_stage(cmd_stage03, "stage03")

    if results["stage03"] != "success":
        return results

    # --------------------------------------------------------------------------
    # Stage 04 — Reporting
    # --------------------------------------------------------------------------
    cmd_stage04 = ["python", "-m", "src.stage04_reporting.run_reporting"]
    results["stage04"] = _run_stage(cmd_stage04, "stage04")

    return results
