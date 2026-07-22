"""
Stage 04 Reporting Runner
================================================================================
Official entrypoint for Stage 04 of the CMS POS/QIES ingestion pipeline.

Responsibilities:
    1. Load Stage 03 intermediate artifacts
    2. Execute Stage 04 reporting engine
    3. Format reporting outputs
    4. Persist Stage 04 processed artifacts into data/stage04_processed/

Design principles:
    - Strong logging for pipeline observability
    - Clear separation between loading, computing, formatting, and writing
    - Deterministic, reproducible pipeline behavior
"""

import logging
from pathlib import Path

from .report_engine import run_report_engine
from .report_formatter import format_reports
from .report_writer import DEFAULT_OUTPUT_DIR, write_reports

# ==============================================================================
# Logging configuration
# ==============================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ==============================================================================
# Stage 04 runner logging (file + console)
# ==============================================================================
fh = logging.FileHandler("logs/runner.log")
fh.setLevel(logging.INFO)
fh.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] stage04_runner: %(message)s")
)
logger.addHandler(fh)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] stage04_runner: %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)


# ==============================================================================
# Stage 03 artifact locations
# ==============================================================================
STAGE03_DIR = Path("data/stage03_intermediate")

QUALITY_SUMMARY_PATH = STAGE03_DIR / "quality_summary.json"
COLUMN_PROFILES_PATH = STAGE03_DIR / "column_profiles.json"
FACILITY_METRICS_PATH = STAGE03_DIR / "facility_metrics.csv"


# ==============================================================================
# Main runner
# ==============================================================================
def main() -> None:
    logger.info("Starting Stage 04 reporting runner...")

    # Validate Stage 03 artifacts exist
    for p in [QUALITY_SUMMARY_PATH, COLUMN_PROFILES_PATH, FACILITY_METRICS_PATH]:
        if not p.exists():
            raise FileNotFoundError(f"Required Stage 03 artifact missing: {p}")

    logger.info("Loading Stage 03 artifacts...")
    logger.info(f" → {QUALITY_SUMMARY_PATH}")
    logger.info(f" → {COLUMN_PROFILES_PATH}")
    logger.info(f" → {FACILITY_METRICS_PATH}")

    logger.info("Executing Stage 04 report engine...")
    report_objects = run_report_engine(
        QUALITY_SUMMARY_PATH,
        COLUMN_PROFILES_PATH,
        FACILITY_METRICS_PATH,
    )

    logger.info("Formatting Stage 04 reporting artifacts...")
    formatted_reports = format_reports(report_objects)

    logger.info(f"Writing Stage 04 processed artifacts → {DEFAULT_OUTPUT_DIR}")
    report_index = write_reports(formatted_reports, base_dir=DEFAULT_OUTPUT_DIR)

    logger.info("Stage 04 reporting completed successfully.")
    logger.info(f"Report index written → {report_index['dataset_summary']}")


if __name__ == "__main__":
    main()
