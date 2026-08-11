"""
Stage 04 Runner
================================================================================
Orchestrates Stage 04 reporting:
    - Loads Stage 03 artifacts
    - Runs report engine
    - Writes Stage 04 processed artifacts

Design principles:
    - Deterministic logging
    - Pure engine + deterministic writer
    - Minimal assumptions about upstream stages
"""

import logging
from pathlib import Path

from src.stage04_reporting.report_engine import run_report_engine
from src.stage04_reporting.report_writer import write_reports
from utils.file_io import ensure_directory

# ==============================================================================
# Module‑level logger placeholder (reconfigured deterministically in main)
# ==============================================================================
logger = logging.getLogger("stage04_runner")


# ==============================================================================
# Deterministic Logging Configuration
# ==============================================================================
def configure_logging(log_path: Path) -> logging.Logger:
    """
    Deterministic logging:
        - No timestamps
        - No levels
        - Overwrite mode
        - UTF‑8
        - Handlers cleared each run
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("stage04_runner")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


# ==============================================================================
# File locations (monkeypatchable by tests)
# ==============================================================================
STAGE03_DIR = Path("data/stage03_intermediate")
QUALITY_SUMMARY_PATH = STAGE03_DIR / "quality_summary.json"
COLUMN_PROFILES_PATH = STAGE03_DIR / "column_profiles.json"
FACILITY_METRICS_PATH = STAGE03_DIR / "facility_metrics.csv"

DEFAULT_OUTPUT_DIR = Path("data/stage04_processed")
LOG_PATH = DEFAULT_OUTPUT_DIR / "stage04.log"  # REQUIRED for tests


# ==============================================================================
# Main runner
# ==============================================================================
def main() -> None:
    logger = configure_logging(LOG_PATH)
    logger.info("STAGE04_LOG_VERSION=1")
    logger.info("Starting Stage 04 reporting runner...")

    logger.info("Loading Stage 03 artifacts...")
    results = run_report_engine(
        QUALITY_SUMMARY_PATH,
        COLUMN_PROFILES_PATH,
        FACILITY_METRICS_PATH,
    )

    logger.info("Ensuring Stage 04 output directory exists...")
    ensure_directory(str(DEFAULT_OUTPUT_DIR))

    logger.info("Writing Stage 04 reporting artifacts...")
    write_reports(results, base_dir=DEFAULT_OUTPUT_DIR)

    logger.info("Stage 04 reporting completed successfully.")
    logger.info(f"Artifacts written to {DEFAULT_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
