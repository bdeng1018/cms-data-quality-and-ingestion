"""
Stage 01 — Automated Schema Regeneration
generate_schema.py
================================================================================
Reads the Stage 02 cleaned_data.csv file and automatically generates a canonical
schema.json containing:
    - field names
    - inferred types (string, integer, float, boolean, date, datetime)

Branch 1 goals:
    - lightweight type inference
    - reproducible schema.json
    - no domain logic
    - safe for Stage 02/03 integration
"""

import json
from pathlib import Path
from typing import Dict

import pandas as pd

from utils.logging_utils import get_logger

logger = get_logger("schema_generator")


# ------------------------------------------------------------------------------
# Type inference helpers
# ------------------------------------------------------------------------------


def infer_type(series: pd.Series) -> str:
    """
    Infer a Stage 01 schema type from a pandas Series.

    Allowed types:
        string, integer, float, boolean, date, datetime
    """

    # Boolean detection
    if series.dropna().isin([True, False]).all():
        return "boolean"

    # Integer detection
    if pd.api.types.is_integer_dtype(series):
        return "integer"

    # Float detection
    if pd.api.types.is_float_dtype(series):
        return "float"

    # Datetime detection
    if pd.api.types.is_datetime64_any_dtype(series):
        # If time component exists → datetime
        if series.dropna().dt.time.astype(str).str.contains(":").any():
            return "datetime"
        return "date"

    # Fallback → string
    return "string"


# ------------------------------------------------------------------------------
# Schema generation
# ------------------------------------------------------------------------------


def generate_schema(cleaned_path: str, out_path: str) -> Dict:
    """
    Generate a schema.json from cleaned_data.csv.

    Parameters
    ----------
    cleaned_path : str
        Path to cleaned_data.csv
    out_path : str
        Output path for schema.json

    Returns
    -------
    dict
        Generated schema dictionary
    """

    cleaned_file = Path(cleaned_path)
    out_file = Path(out_path)

    if not cleaned_file.exists():
        raise FileNotFoundError(f"Cleaned data file not found: {cleaned_path}")

    logger.info(f"Loading cleaned data from: {cleaned_path}")
    df = pd.read_csv(cleaned_file)

    logger.info(f"Inferring schema for {df.shape[1]} columns...")

    fields = []
    for col in df.columns:
        inferred = infer_type(df[col])
        fields.append({"name": col, "type": inferred})
        logger.info(f"Inferred type for '{col}': {inferred}")

    schema = {"fields": fields}

    logger.info(f"Writing schema to: {out_path}")
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with out_file.open("w") as f:
        json.dump(schema, f, indent=2)

    logger.info("Schema regeneration complete.")
    return schema


# ------------------------------------------------------------------------------
# CLI entrypoint
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Stage 01 schema.json")
    parser.add_argument("--cleaned", required=True, help="Path to cleaned_data.csv")
    parser.add_argument("--out", required=True, help="Output schema.json path")

    args = parser.parse_args()

    generate_schema(args.cleaned, args.out)
