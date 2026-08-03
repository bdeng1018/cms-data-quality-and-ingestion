"""
Stage 05 — Pipeline Runner
================================================================================

This module provides the CLI entrypoint for Stage 05 of the CMS Data Quality &
Ingestion Pipeline. It is responsible for:

- Loading pipeline configuration
- Starting the pipeline timer
- Executing the orchestrator (Stage 01 → Stage 02 → Stage 03 → Stage 04)
- Validating outputs from Stage 04 (data/stage04_processed/)
- Generating the final pipeline summary JSON
- Writing the summary to data/stage05_reports/

This script is intentionally minimal and deterministic.
"""

import argparse
import datetime
import json
import logging
from pathlib import Path

from .config_loader import load_pipeline_config
from .orchestrator import run_all_stages

# ==============================================================================
# Logging setup
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Stage05] %(levelname)s: %(message)s",
)


# ==============================================================================
# Custom ArgumentParser to match test expectations
# ==============================================================================
class Stage05ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise SystemExit(1)


# ==============================================================================
# Write summary JSON
# ==============================================================================
def write_summary(summary_path, summary_dict):
    summary_path = Path(summary_path)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    with summary_path.open("w") as f:
        f.write(json.dumps(summary_dict, indent=2))


# ==============================================================================
# Validate Stage 04 outputs
# ==============================================================================
def validate_stage04_outputs(root: Path | None = None):
    if root is None:
        root = Path(__file__).resolve().parents[2]

    required = [
        root / "data" / "stage04_processed" / "report_index.json",
        root / "data" / "stage04_processed" / "facility_health.csv",
        root / "data" / "stage04_processed" / "dataset_summary.json",
    ]

    return [str(p) for p in required if not p.exists()]


# ==============================================================================
# Main entrypoint
# ==============================================================================
def main():
    root = Path(__file__).resolve().parents[2]

    parser = Stage05ArgumentParser(
        description="Stage 05 Pipeline Runner — CMS Data Quality & Ingestion"
    )
    parser.add_argument(
        "--config",
        required=False,
        default="configs/pipeline.yml",
    )
    parser.add_argument(
        "--output",
        required=False,
        default="data/stage05_reports/pipeline_summary.json",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / args.config

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = root / args.output

    logging.info(f"Using config: {config_path}")
    logging.info(f"Summary output: {output_path}")

    # --------------------------------------------------------------------------
    # Config existence check (Fixes test_cli_nonexistent_config)
    # --------------------------------------------------------------------------
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # --------------------------------------------------------------------------
    # Load configuration
    # --------------------------------------------------------------------------
    try:
        config = load_pipeline_config(config_path)
    except Exception as e:
        summary = {
            "pipeline": "cms-data-quality-and-ingestion",
            "timestamp_start": None,
            "timestamp_end": None,
            "duration_seconds": 0.0,
            "stages": {
                "stage01": "skipped",
                "stage02": "skipped",
                "stage03": "skipped",
                "stage04": "skipped",
            },
            "warnings": [f"Failed to load config: {str(e)}"],
        }
        write_summary(output_path, summary)
        return

    # --------------------------------------------------------------------------
    # Start timer
    # --------------------------------------------------------------------------
    start_dt = datetime.datetime.now()
    timestamp_start = start_dt.isoformat()

    # --------------------------------------------------------------------------
    # Execute orchestrator (Fixes fail-fast SystemExit)
    # --------------------------------------------------------------------------
    try:
        stage_results = run_all_stages(config)
    except Exception as e:
        end_dt = datetime.datetime.now()
        summary = {
            "pipeline": "cms-data-quality-and-ingestion",
            "timestamp_start": timestamp_start,
            "timestamp_end": end_dt.isoformat(),
            "duration_seconds": (end_dt - start_dt).total_seconds(),
            "stages": {
                "stage01": "failed",
                "stage02": "skipped",
                "stage03": "skipped",
                "stage04": "skipped",
            },
            "warnings": [f"Pipeline aborted due to error: {str(e)}"],
        }
        write_summary(output_path, summary)
        return

    # --------------------------------------------------------------------------
    # Validate Stage 04 outputs
    # --------------------------------------------------------------------------
    missing = validate_stage04_outputs(root=root)
    warnings = []

    if missing:
        warnings.append("Missing Stage 04 artifacts: " + ", ".join(missing))

    # --------------------------------------------------------------------------
    # Stop timer
    # --------------------------------------------------------------------------
    end_dt = datetime.datetime.now()

    # --------------------------------------------------------------------------
    # Build summary
    # --------------------------------------------------------------------------
    summary = {
        "pipeline": "cms-data-quality-and-ingestion",
        "timestamp_start": timestamp_start,
        "timestamp_end": end_dt.isoformat(),
        "duration_seconds": (end_dt - start_dt).total_seconds(),
        "stages": stage_results,
        "warnings": warnings,
    }

    # --------------------------------------------------------------------------
    # Write summary JSON (Fixes summary-written-once)
    # --------------------------------------------------------------------------
    write_summary(output_path, summary)


if __name__ == "__main__":
    main()
