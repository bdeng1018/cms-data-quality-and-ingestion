"""
Stage 03 Quality Writer
================================================================================
Responsible for persisting all intermediate artifacts produced by the Stage 03
quality engine. These artifacts are consumed by Stage 04 (reporting) and Stage 05
(pipeline runner).

Artifacts written:
    - quality_summary.json      (dataset-level metrics)
    - facility_metrics.csv      (facility-level metrics)
    - column_profiles.json      (column-level metrics)

Design principles:
    - Pure I/O: no computation happens here.
    - Strong typing and validation.
    - Structured logging for pipeline observability.
    - Directory safety: auto-create target folder.
    - Test isolation: writers accept a base_dir parameter so pytest never writes
      into the real pipeline directories.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] stage03_quality_writer: %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# ==============================================================================
# NumPy conversion
# ==============================================================================


def to_python_scalar(value):
    """Convert numpy scalar types to native Python types."""
    if isinstance(value, np.generic):
        return value.item()
    return value


# ==============================================================================
# Default directory (pipeline only)
# ==============================================================================
DEFAULT_INTERMEDIATE_DIR = Path("data/stage03_intermediate")


def ensure_dir(base_dir: Path) -> None:
    """
    Ensure the target directory exists.
    Tests pass tmp_path here; pipeline uses DEFAULT_INTERMEDIATE_DIR.
    """
    if not base_dir.exists():
        logger.info(f"Creating intermediate directory: {base_dir}")
        base_dir.mkdir(parents=True, exist_ok=True)
    else:
        logger.info(f"Intermediate directory already exists: {base_dir}")


# ==============================================================================
# Dataset-level metrics writer
# ==============================================================================
def write_quality_summary(summary: dict, base_dir: Path = DEFAULT_INTERMEDIATE_DIR):
    """
    Write dataset-level quality metrics to JSON.
    Tests override base_dir to avoid polluting real pipeline directories.
    """
    ensure_dir(base_dir)
    out_path = base_dir / "quality_summary.json"

    logger.info(f"Writing dataset-level quality summary → {out_path}")

    clean_summary = {k: to_python_scalar(v) for k, v in summary.items()}

    with out_path.open("w") as f:
        json.dump(clean_summary, f, indent=2)

    logger.info("Dataset-level quality summary written successfully.")


# ==============================================================================
# Facility-level metrics writer
# ==============================================================================
def write_facility_metrics(
    df_facility: pd.DataFrame, base_dir: Path = DEFAULT_INTERMEDIATE_DIR
) -> None:
    """
    Write facility-level metrics to CSV.
    """
    ensure_dir(base_dir)
    out_path = base_dir / "facility_metrics.csv"

    logger.info(f"Writing facility-level metrics → {out_path}")

    df_facility.to_csv(out_path, index=False)

    logger.info("Facility-level metrics written successfully.")


# ==============================================================================
# Column-level metrics writer
# ==============================================================================
def write_column_profiles(profiles: dict, base_dir: Path = DEFAULT_INTERMEDIATE_DIR):
    """
    Write column-level profiles to JSON.
    """
    ensure_dir(base_dir)
    out_path = base_dir / "column_profiles.json"

    logger.info(f"Writing column-level profiles → {out_path}")

    clean_profiles = {
        col: {k: to_python_scalar(v) for k, v in stats.items()}
        for col, stats in profiles.items()
    }

    with out_path.open("w") as f:
        json.dump(clean_profiles, f, indent=2)

    logger.info("Column-level profiles written successfully.")


# ==============================================================================
# Optional: Write all artifacts in one call
# ==============================================================================
def write_all_artifacts(
    summary_dict: Dict[str, Any],
    df_facility: pd.DataFrame,
    column_profiles: Dict[str, Dict[str, Any]],
    base_dir: Path = DEFAULT_INTERMEDIATE_DIR,
) -> None:
    """
    Convenience function to write all Stage 03 artifacts in one call.
    Tests override base_dir to isolate outputs.
    """
    logger.info("Writing all Stage 03 artifacts...")
    write_quality_summary(summary_dict, base_dir=base_dir)
    write_facility_metrics(df_facility, base_dir=base_dir)
    write_column_profiles(column_profiles, base_dir=base_dir)
    logger.info("All Stage 03 artifacts written successfully.")
