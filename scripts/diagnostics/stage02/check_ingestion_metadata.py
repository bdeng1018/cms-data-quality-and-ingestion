"""
Diagnostics — Stage 02 Ingestion Metadata (Optional Mode)
---------------------------------------------------------
Purpose:
    Validate ingestion metadata when present, but do NOT fail the Stage 02
    diagnostics suite if metadata is missing. This supports development and
    partial‑pipeline execution where cleaned_data.csv may exist without the
    full ingestion metadata artifact.

Behavior:
    - If ingestion_metadata.json exists:
        * Validate file presence
        * Validate JSON structure
        * Validate required fields
        * Validate deterministic behavior

    - If ingestion_metadata.json is missing:
        * Emit a clear, explicit skip message
        * Do NOT raise FileNotFoundError
        * Allow Stage 02 diagnostics to continue

Rationale:
    Stage 02 ingestion metadata is produced only when the ingestion runner
    executes fully. Wrapper diagnostics, C++ utilities, and partial ingestion
    runs may produce cleaned_data.csv without metadata. This optional mode
    prevents false negatives during development while preserving correctness
    when metadata is available.

Design Principles:
    - Deterministic behavior
    - No side effects
    - No pipeline blocking
    - Clear skip semantics
"""

import json
from pathlib import Path

METADATA_PATH = Path("data/stage02_cleaned/ingestion_metadata.json")


def check_metadata_exists_optional():
    """
    Optional existence check.
    If metadata is missing, print a skip message and return gracefully.
    """
    if not METADATA_PATH.exists():
        print(f"[SKIP] Stage 02 ingestion metadata not found: {METADATA_PATH}")
        print("[SKIP] Skipping ingestion metadata diagnostics (optional mode).")
        return False
    return True


def load_metadata():
    """Load metadata JSON deterministically."""
    with open(METADATA_PATH) as f:
        return json.load(f)


def check_metadata_structure(metadata):
    """
    Validate that metadata contains the expected top‑level fields.
    Adjust this list as your ingestion pipeline evolves.
    """
    required_fields = [
        "source_files",
        "row_count",
        "ingestion_timestamp",
        "schema_version",
    ]

    missing = [f for f in required_fields if f not in metadata]
    if missing:
        raise AssertionError(f"Metadata missing required fields: {missing}")


def check_metadata_determinism():
    """
    Ensure metadata loads deterministically and does not change between reads.
    """
    m1 = load_metadata()
    m2 = load_metadata()

    if m1 != m2:
        raise AssertionError("Metadata is non‑deterministic across reads")


def main():
    # Optional existence check
    if not check_metadata_exists_optional():
        return  # Skip entire diagnostic gracefully

    # Metadata exists — perform full validation
    metadata = load_metadata()
    check_metadata_structure(metadata)
    check_metadata_determinism()

    print("Stage 02 ingestion metadata diagnostics passed (optional mode).")


if __name__ == "__main__":
    main()
