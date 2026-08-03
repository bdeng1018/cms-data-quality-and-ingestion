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

Stage 05 does NOT produce its own log file. Logging remains stage-scoped:
    logs/ingestion.log   # Stage 02
    logs/quality.log     # Stage 03
    logs/runner.log      # Stage 04

This script is intentionally minimal and deterministic.
"""

import argparse
import datetime
import json
import logging
import os
import sys
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
        # Tests expect SystemExit(1) for CLI argument errors
        raise SystemExit(1)


# ==============================================================================
# Write summary JSON
# ==============================================================================
def write_summary(summary_path, summary_dict):
    """Write the pipeline summary JSON to Stage 05 output directory."""
    summary_path = Path(summary_path)

    # Ensure parent directory exists
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.touch(exist_ok=True)

    with summary_path.open("w") as f:
        f.write(json.dumps(summary_dict, indent=2))


# ==============================================================================
# Validate Stage 04 outputs
# ==============================================================================
def validate_stage04_outputs(root: Path | None = None):
    """
    Stage 05 must confirm Stage 04 produced its required artifacts.

    Required files:
        data/stage04_processed/report_index.json
        data/stage04_processed/facility_health.csv
        data/stage04_processed/dataset_summary.json

    Stage 05 does NOT read raw data, cleaned data, or intermediate artifacts.
    """
    if root is None:
        root = Path(__file__).resolve().parents[2]

    required = [
        root / "data" / "stage04_processed" / "report_index.json",
        root / "data" / "stage04_processed" / "facility_health.csv",
        root / "data" / "stage04_processed" / "dataset_summary.json",
    ]

    missing = [str(p) for p in required if not p.exists()]
    return missing


# ==============================================================================
# Main entrypoint
# ==============================================================================
def main():
    root = Path(__file__).resolve().parents[2]

    # --------------------------------------------------------------------------
    # Parse CLI arguments
    # --------------------------------------------------------------------------
    parser = Stage05ArgumentParser(
        description="Stage 05 Pipeline Runner — CMS Data Quality & Ingestion"
    )
    parser.add_argument(
        "--config",
        required=False,
        default="configs/pipeline.yml",
        help="Path to pipeline.yml configuration file (default: configs/pipeline.yml)",
    )
    parser.add_argument(
        "--output",
        required=False,
        default="data/stage05_reports/pipeline_summary.json",
        help=(
            "Path to pipeline_summary.json output file "
            "(default: data/stage05_reports/pipeline_summary.json)"
        ),
    )
    args = parser.parse_args()

    # Resolve paths relative to project root if not absolute
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / args.config

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = root / args.output

    logging.info(f"Using config: {config_path}")
    logging.info(f"Summary output: {output_path}")

    # --------------------------------------------------------------------------
    # Load configuration
    # --------------------------------------------------------------------------
    try:
        config = load_pipeline_config(config_path)
    except Exception as e:
        logging.error(f"Failed to load pipeline config from {config_path}: {e}")
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
        print(f"[Stage05] Config load failed. Summary written to {output_path}")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # Start pipeline timer
    # --------------------------------------------------------------------------
    start_dt = datetime.datetime.now()
    timestamp_start = start_dt.isoformat()
    logging.info("Pipeline execution started.")

    # --------------------------------------------------------------------------
    # Execute orchestrator (Stage 01 → Stage 02 → Stage 03 → Stage 04)
    # --------------------------------------------------------------------------
    try:
        stage_results = run_all_stages(config)
    except Exception as e:
        end_dt = datetime.datetime.now()
        timestamp_end = end_dt.isoformat()
        duration = (end_dt - start_dt).total_seconds()

        logging.error(f"Pipeline aborted due to error: {e}")

        summary = {
            "pipeline": "cms-data-quality-and-ingestion",
            "timestamp_start": timestamp_start,
            "timestamp_end": timestamp_end,
            "duration_seconds": duration,
            "stages": {
                "stage01": "failed",
                "stage02": "skipped",
                "stage03": "skipped",
                "stage04": "skipped",
            },
            "warnings": [f"Pipeline aborted due to error: {str(e)}"],
        }

        write_summary(output_path, summary)
        print(f"[Stage05] Pipeline aborted. Summary written to {output_path}")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # Validate Stage 04 outputs
    # --------------------------------------------------------------------------
    missing = validate_stage04_outputs(root=root)
    warnings: list[str] = []

    if missing:
        msg = "Missing Stage 04 artifacts: " + ", ".join(missing)
        logging.warning(msg)
        warnings.append(msg)

    # --------------------------------------------------------------------------
    # Stop timer
    # --------------------------------------------------------------------------
    end_dt = datetime.datetime.now()
    timestamp_end = end_dt.isoformat()
    duration = (end_dt - start_dt).total_seconds()
    logging.info("Pipeline execution completed.")

    # --------------------------------------------------------------------------
    # Build summary artifact
    # --------------------------------------------------------------------------
    summary = {
        "pipeline": "cms-data-quality-and-ingestion",
        "timestamp_start": timestamp_start,
        "timestamp_end": timestamp_end,
        "duration_seconds": duration,
        "stages": stage_results,
        "warnings": warnings,
    }

    # --------------------------------------------------------------------------
    # Write summary JSON
    # --------------------------------------------------------------------------
    write_summary(output_path, summary)

    print("[Stage05] Pipeline completed successfully.")
    print(f"[Stage05] Summary written to: {output_path}")


if __name__ == "__main__":
    main()