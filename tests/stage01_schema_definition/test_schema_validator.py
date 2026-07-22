"""
Tests for Stage 01 — Schema Validator

These tests verify the behavior of the helper validation functions used
in Stage 01 to check for duplicate field names, missing type definitions,
and invalid type values in the canonical schema.
"""

from src.stage01_schema_definition.schema_validator import (
    check_for_duplicate_fields,
    check_for_invalid_types,
    check_for_missing_types,
)


def test_no_duplicate_fields():
    """
    Ensure that no duplicates are reported when all field names are unique.
    """
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "integer"},
    ]
    duplicates = check_for_duplicate_fields(fields)
    assert duplicates == []


def test_detect_duplicate_fields():
    """
    Verify that duplicate field names are correctly identified.
    """
    fields = [
        {"name": "a", "type": "string"},
        {"name": "a", "type": "integer"},
    ]
    duplicates = check_for_duplicate_fields(fields)
    assert duplicates == ["a"]


def test_no_missing_types():
    """
    Ensure that no missing types are reported when all fields define a type.
    """
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "integer"},
    ]
    missing = check_for_missing_types(fields)
    assert missing == []


def test_detect_missing_types():
    """
    Verify that fields missing a type definition are correctly identified.
    """
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": ""},
        {"name": "c"},
    ]
    missing = check_for_missing_types(fields)
    assert missing == ["b", "c"]


def test_no_invalid_types():
    """
    Ensure that no invalid types are reported when all types are allowed.
    """
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "integer"},
        {"name": "c", "type": "boolean"},
    ]
    invalid = check_for_invalid_types(fields)
    assert invalid == []


def test_detect_invalid_types():
    """
    Verify that invalid type values are correctly identified.
    """
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "banana"},
        {"name": "c", "type": "float"},
        {"name": "d", "type": "unknown"},
    ]
    invalid = check_for_invalid_types(fields)
    assert invalid == ["banana", "unknown"]
