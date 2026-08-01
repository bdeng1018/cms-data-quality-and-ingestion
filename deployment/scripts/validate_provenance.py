#!/usr/bin/env python3
"""
validate_provenance.py

Validates manifest.provenance against MANIFEST_SPEC.md.

This validator enforces:
- required fields exist
- fields are non-empty
- semantic versioning (X.Y.Z)
- deterministic validation output
- structured logging for CI/CD

It does NOT enforce business logic; that lives in MANIFEST_SPEC.md.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "pipeline_version",
    "schema_version",
    "artifact_version",
    "manifest_version",
    "deployment_version",
    "sbom_version",
]

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def load_json(path: Path):
    """Load JSON with deterministic error handling."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load JSON '{path}': {e}")
        sys.exit(1)


def validate_semver(name: str, value: str):
    """Validate semantic versioning (X.Y.Z)."""
    if not SEMVER_PATTERN.match(value):
        print(f"[ERROR] {name}='{value}' is not valid semantic versioning (X.Y.Z).")
        return False
    print(f"[OK] {name}='{value}' is valid semantic versioning.")
    return True


def validate_required_fields(manifest: dict):
    """Validate required fields exist and are non-empty."""
    print("[INFO] Checking required fields...")
    ok = True
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            print(f"[ERROR] Missing required field: {field}")
            ok = False
        elif manifest[field] in ("", None):
            print(f"[ERROR] Field '{field}' is empty.")
            ok = False
        else:
            print(f"[OK] Field '{field}' present.")
    return ok


def validate_versions(manifest: dict):
    """Validate all version fields follow semantic versioning."""
    print("[INFO] Checking semantic versioning...")
    ok = True
    for field in REQUIRED_FIELDS:
        value = manifest.get(field, "")
        if not validate_semver(field, value):
            ok = False
    return ok


def main():
    parser = argparse.ArgumentParser(description="Validate manifest.provenance")
    parser.add_argument("--manifest", required=True, help="Path to manifest.provenance")
    parser.add_argument("--spec", required=True, help="Path to MANIFEST_SPEC.md")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    spec_path = Path(args.spec)

    if not manifest_path.exists():
        print(f"[ERROR] Manifest file not found: {manifest_path}")
        sys.exit(1)

    if not spec_path.exists():
        print(f"[ERROR] Spec file not found: {spec_path}")
        sys.exit(1)

    print("=== Provenance Validation ===")
    manifest = load_json(manifest_path)

    ok_required = validate_required_fields(manifest)
    ok_versions = validate_versions(manifest)

    print("\n=== Validation Summary ===")
    if ok_required and ok_versions:
        print("[OK] manifest.provenance is valid.")
        sys.exit(0)
    else:
        print("[FAIL] manifest.provenance failed validation.")
        sys.exit(2)


if __name__ == "__main__":
    main()
