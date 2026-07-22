"""
Stage 01 — Schema Definition
schema_loader.py
================================================================================
Responsible for loading the POS–QIES schema.json file and exposing it as a Python
dictionary for downstream ingestion, cleaning, and quality stages.

Branch 1 design:
    - Lightweight loader
    - No validation beyond file existence + basic structure
    - No domain logic
"""

import json
from pathlib import Path
from typing import Any, Dict

from utils.logging_utils import get_logger

logger = get_logger("schema_loader")


def load_schema(schema_path: str = "data/stage01_schema/schema.json") -> Dict[str, Any]:
    """
    Load the POS–QIES schema.json file.

    Parameters
    ----------
    schema_path : str
        Path to the schema JSON file.

    Returns
    -------
    dict
        Parsed schema dictionary with required key: "fields".
    """
    path = Path(schema_path)

    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    logger.info(f"Loading schema from: {schema_path}")

    with path.open("r") as f:
        schema = json.load(f)

    # Basic structural validation (Branch 1)
    if "fields" not in schema:
        raise KeyError("Schema JSON missing required key: 'fields'")

    if not isinstance(schema["fields"], list):
        raise TypeError("Schema 'fields' must be a list of field definitions.")

    logger.info(f"Schema loaded successfully with {len(schema['fields'])} fields.")
    return schema
