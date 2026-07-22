"""
Stage 01 — Schema Definition
schema_validator.py

Provides structural and type validation for the canonical Stage 01 schema.
Checks include:
- required keys exist
- no duplicate field names
- all fields define a valid type
- schema is well‑formed

This module is intentionally minimal for Branch 1 and serves as the
foundation for all future ingestion and quality stages.
"""

VALID_TYPES = {
    "string",
    "integer",
    "float",
    "boolean",
    "date",
    "datetime",
}
"""Set of allowed field types for Stage 01 schema validation."""


def validate_schema(schema: dict) -> list:
    """
    Validate the full schema dictionary.

    This function performs all Stage 01 validation checks:
    - ensures the top-level 'fields' key exists
    - checks for duplicate field names
    - checks for missing type definitions
    - checks for invalid type values

    Parameters
    ----------
    schema : dict
        Parsed schema dictionary loaded from JSON.

    Returns
    -------
    list
        A list of validation error messages.
        Empty list means the schema is valid.
    """
    errors = []

    # Check top-level structure
    if "fields" not in schema:
        errors.append("Missing top-level key: 'fields'")
        return errors

    fields = schema["fields"]

    # Check duplicates
    seen = set()
    for col in fields:
        name = col.get("name")
        if name in seen:
            errors.append(f"Duplicate field/column name: {name}")
        seen.add(name)

        # Check required fields
        if "type" not in col:
            errors.append(f"Field/Column '{name}' missing required key: type")

        # Validate type
        if col.get("type") not in VALID_TYPES:
            errors.append(f"Field/Column '{name}' has invalid type: {col.get('type')}")

    return errors


def check_for_duplicate_fields(fields: list) -> list:
    """
    Identify duplicate field names in the schema.

    Parameters
    ----------
    fields : list
        List of field dictionaries from the schema.

    Returns
    -------
    list
        List of duplicate field names.
        Empty list means no duplicates were found.
    """
    seen = set()
    duplicates = []
    for f in fields:
        name = f.get("name")
        if name in seen:
            duplicates.append(name)
        else:
            seen.add(name)
    return duplicates


def check_for_missing_types(fields: list) -> list:
    """
    Identify fields that do not define a 'type' key.

    Parameters
    ----------
    fields : list
        List of field dictionaries from the schema.

    Returns
    -------
    list
        List of field names missing a type definition.
        Empty list means all fields define a type.
    """
    missing = []
    for f in fields:
        t = f.get("type")
        if not t:
            missing.append(f.get("name"))
    return missing


def check_for_invalid_types(fields: list) -> list:
    """
    Identify fields whose type is not one of the allowed Stage 01 types.

    Parameters
    ----------
    fields : list
        List of field dictionaries from the schema.

    Returns
    -------
    list
        List of invalid type values.
        Empty list means all types are valid.
    """
    allowed = {"string", "integer", "float", "boolean", "date", "datetime"}
    invalid = []
    for f in fields:
        t = f.get("type")
        if t not in allowed:
            invalid.append(t)
    return invalid
