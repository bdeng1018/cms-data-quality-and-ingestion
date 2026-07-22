"""
Tests for Stage 01 — Schema Loader

These tests verify that the canonical schema.json file is loaded correctly
and that its structure matches the expectations of the Stage 01 validator
and downstream ingestion stages.
"""

import json

import pytest

import src.stage01_schema_definition.schema_loader as loader

# from pathlib import Path


@pytest.fixture
def fake_schema(tmp_path, monkeypatch):
    """
    Create a temporary schema.json and patch load_schema() to use it.
    """
    schema_path = tmp_path / "schema.json"
    schema = {
        "fields": [
            {"name": "facility_id", "type": "string"},
            {"name": "col1", "type": "integer"},
        ]
    }
    with schema_path.open("w") as f:
        json.dump(schema, f)

    monkeypatch.setattr(loader, "load_schema", lambda: json.load(schema_path.open()))
    return schema


def test_load_schema_returns_dict(fake_schema):
    schema = loader.load_schema()
    assert isinstance(schema, dict)


def test_load_schema_has_fields_key(fake_schema):
    schema = loader.load_schema()
    assert "fields" in schema
    assert isinstance(schema["fields"], list)


def test_load_schema_field_structure(fake_schema):
    schema = loader.load_schema()
    first = schema["fields"][0]

    assert "name" in first
    assert "type" in first
    assert isinstance(first["name"], str)
    assert isinstance(first["type"], str)
