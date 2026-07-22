"""
Stage 01 — Schema Definition
schema_loader.py

Responsible for loading the POS–QIES schema.json file and exposing it
as a Python dictionary for downstream ingestion, normalization, and
data‑quality stages.

This module intentionally stays lightweight in Branch 1.
"""

import json
from pathlib import Path


def load_schema(schema_path: str = "data/stage01_schema/schema.json") -> dict:
    """
    Load the POS–QIES schema.json file.

    Parameters
    ----------
    schema_path : str
        Path to the schema JSON file.

    Returns
    -------
    dict
        Parsed schema dictionary.
    """
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(path, "r") as f:
        schema = json.load(f)

    return schema
