"""
run_ingestion.py
Stage 02 — Local Ingestion Runner (POS-Only, Pipeline-Compatible)
================================================================================
Branch 1 MVP: Only POS ingestion is supported.

Responsibilities:
- Auto-discover raw POS file
- Load raw POS dataset
- Validate minimal structure (rows > 0, columns > 0)
- Log ingestion results
- Write cleaned output for downstream stages
"""

import sys
from pathlib import Path

import pandas as pd

from stage02_raw_ingestion.pos_ingestion import PosIngestionSource
from utils.logging_utils import get_logger

logger = get_logger("run_ingestion")


# ==============================================================================
# POS ingestion
# ==============================================================================
def run_pos_ingestion(path: Path) -> pd.DataFrame:
    logger.info(f"Running POS ingestion for file: {path}")
    pos = PosIngestionSource(str(path))
    df = pos.load_raw()
    pos.validate_minimal_structure(df)
    logger.info(f"POS ingestion complete. Shape: {df.shape}")
    return df


# ==============================================================================
# Pipeline-Compatible Entrypoint (POS-only)
# ==============================================================================
def run_ingestion_pipeline() -> None:
    """
    Auto-ingest POS raw file.

    This function is called by Stage 05 and must not require CLI arguments.
    """

    raw_dir = Path("data/stage02_raw")
    pos_path = raw_dir / "pos_q2_2026.parquet"

    if not pos_path.exists():
        logger.error(f"Missing POS raw file: {pos_path}")
        sys.exit(1)

    pos_df = run_pos_ingestion(pos_path)

    output_path = Path("data/stage02_cleaned/cleaned_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pos_df.to_csv(output_path, index=False)

    logger.info(f"Stage 02 ingestion complete. Output written to: {output_path}")


# ==============================================================================
# Main
# ==============================================================================
if __name__ == "__main__":
    # Pipeline-compatible: no CLI args required
    run_ingestion_pipeline()
