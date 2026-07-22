"""
Tests for Stage 01 — Schema Loader

These tests verify that the canonical schema.json file is loaded correctly
and that its structure matches the expectations of the Stage 01 validator
and downstream ingestion stages.
"""

from src.stage01_schema_definition.schema_loader import load_schema


def test_load_schema_returns_dict():
    """
    Ensure that load_schema() returns a Python dictionary.

    This confirms that the JSON file is parsed correctly and that the loader
    exposes the schema in a usable Python structure.
    """
    schema = load_schema()
    assert isinstance(schema, dict)


def test_load_schema_has_fields_key():
    """
    Verify that the loaded schema contains the required top-level 'fields' key.

    The Stage 01 validator depends on this key to perform structural checks.
    """
    schema = load_schema()
    assert "fields" in schema
    assert isinstance(schema["fields"], list)


def test_load_schema_field_structure():
    """
    Validate the structure of the first field entry in the schema.

    Each field must define:
    - 'name' (string)
    - 'type' (string)

    This ensures the schema adheres to the canonical Stage 01 format.
    """
    schema = load_schema()
    first = schema["fields"][0]

    assert "name" in first
    assert "type" in first
    assert isinstance(first["name"], str)
    assert isinstance(first["type"], str)
