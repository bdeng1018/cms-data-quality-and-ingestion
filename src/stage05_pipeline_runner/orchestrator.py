"""
Stage 05 — Orchestrator
================================================================================

This module defines the orchestrator for Stage 05 of the CMS Data Quality &
Ingestion Pipeline. It executes Stages 01–04 in deterministic order:

    Stage 01 → Stage 02 → Stage 03 → Stage 04

The orchestrator does NOT perform timing, logging, or summary writing.
Those responsibilities belong to run_pipeline.py.

The orchestrator returns a dictionary describing the success/failure
status of each stage, which is used by Stage 05 to build the final
pipeline summary JSON.
"""

import subprocess


# ------------------------------------------------------------------------------
# Helper: run a stage command
# ------------------------------------------------------------------------------
def _run_stage(cmd, stage_name):
    """
    Execute a stage command using subprocess.

    Parameters
    ----------
    cmd : list[str]
        The command to execute, e.g. ["python", "src/stage02_raw_ingestion/run_ingestion.py"]
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


# ------------------------------------------------------------------------------
# Orchestrator: run all stages in correct order
# ------------------------------------------------------------------------------
def run_all_stages(config):
    """
    Execute Stage 01 → Stage 02 → Stage 03 → Stage 04 in deterministic order.

    Stage commands are defined here explicitly to keep Stage 05 simple and
    predictable. Stage 05 does NOT mutate any data; it only executes stages
    and returns their status.

    Parameters
    ----------
    config : dict
        Parsed pipeline.yml configuration.

    Returns
    -------
    dict
        {
            "stage01": "success" | "failed",
            "stage02": "success" | "failed",
            "stage03": "success" | "failed",
            "stage04": "success" | "failed"
        }
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
    cmd_stage01 = ["python", "src/stage01_schema_definition/schema_loader.py"]
    results["stage01"] = _run_stage(cmd_stage01, "stage01")

    if results["stage01"] != "success":
        return results

    # --------------------------------------------------------------------------
    # Stage 02 — Raw Ingestion + Cleaning
    # --------------------------------------------------------------------------
    cmd_stage02 = ["python", "src/stage02_raw_ingestion/run_ingestion.py"]
    results["stage02"] = _run_stage(cmd_stage02, "stage02")

    if results["stage02"] != "success":
        return results

    # --------------------------------------------------------------------------
    # Stage 03 — Data Quality
    # --------------------------------------------------------------------------
    cmd_stage03 = ["python", "src/stage03_data_quality/run_quality.py"]
    results["stage03"] = _run_stage(cmd_stage03, "stage03")

    if results["stage03"] != "success":
        return results

    # --------------------------------------------------------------------------
    # Stage 04 — Reporting
    # --------------------------------------------------------------------------
    cmd_stage04 = ["python", "src/stage04_reporting/run_reporting.py"]
    results["stage04"] = _run_stage(cmd_stage04, "stage04")

    return results
