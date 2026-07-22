"""
Diagnostics — Stage 01
check_schema.py

Runs schema loading + validation and prints results.
Used for quick smoke checks during development.
"""

from src.stage01_schema_definition.schema_loader import load_schema
from src.stage01_schema_definition.schema_validator import validate_schema


def run():
    print("Running Stage 01 — Schema Diagnostics...\n")

    schema = load_schema()
    errors = validate_schema(schema)

    if not errors:
        print("✓ Schema is valid.")
    else:
        print("✗ Schema has validation issues:")
        for err in errors:
            print(f"  - {err}")


if __name__ == "__main__":
    run()
