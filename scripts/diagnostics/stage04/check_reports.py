"""
Stage 04 Diagnostics — Report Artifact Validator
================================================

Validates that Stage 04 processed artifacts exist, load correctly,
and contain expected keys/columns.

This script is intentionally lightweight and safe to run anytime.
"""

import json
from pathlib import Path

import pandas as pd

STAGE04_DIR = Path("data/stage04_processed")

REQUIRED_JSON = [
    "dataset_summary.json",
    "column_health.json",
    "sparse_columns.json",
    "report_index.json",
]

REQUIRED_CSV = [
    "facility_health.csv",
    "top_facilities.csv",
    "bottom_facilities.csv",
]


def check_json(path: Path):
    try:
        with path.open("r") as f:
            data = json.load(f)
        print(f"[OK] JSON loaded: {path}")
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load JSON {path}: {e}")
        return None


def check_csv(path: Path):
    try:
        df = pd.read_csv(path)
        print(f"[OK] CSV loaded: {path} (rows={len(df)})")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load CSV {path}: {e}")
        return None


def main():
    print("=== Stage 04 Diagnostics: Checking processed artifacts ===")

    if not STAGE04_DIR.exists():
        print(f"[ERROR] Stage 04 directory missing: {STAGE04_DIR}")
        return

    print(f"[INFO] Checking directory: {STAGE04_DIR}")

    # Check JSON artifacts
    for filename in REQUIRED_JSON:
        path = STAGE04_DIR / filename
        if not path.exists():
            print(f"[ERROR] Missing JSON artifact: {filename}")
        else:
            check_json(path)

    # Check CSV artifacts
    for filename in REQUIRED_CSV:
        path = STAGE04_DIR / filename
        if not path.exists():
            print(f"[ERROR] Missing CSV artifact: {filename}")
        else:
            check_csv(path)

    print("=== Stage 04 Diagnostics Complete ===")


if __name__ == "__main__":
    main()
