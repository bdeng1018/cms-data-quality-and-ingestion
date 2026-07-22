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
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "integer"},
    ]
    assert check_for_duplicate_fields(fields) == []


def test_detect_duplicate_fields():
    fields = [
        {"name": "a", "type": "string"},
        {"name": "a", "type": "integer"},
    ]
    assert check_for_duplicate_fields(fields) == ["a"]


def test_no_missing_types():
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "integer"},
    ]
    assert check_for_missing_types(fields) == []


def test_detect_missing_types():
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": ""},
        {"name": "c"},
    ]
    assert check_for_missing_types(fields) == ["b", "c"]


def test_no_invalid_types():
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "integer"},
        {"name": "c", "type": "boolean"},
    ]
    assert check_for_invalid_types(fields) == []


def test_detect_invalid_types():
    fields = [
        {"name": "a", "type": "string"},
        {"name": "b", "type": "banana"},
        {"name": "c", "type": "float"},
        {"name": "d", "type": "unknown"},
    ]
    assert check_for_invalid_types(fields) == ["banana", "unknown"]
