#!/usr/bin/env python3
"""
validate_sbom.py

Validates SBOM JSON against SBOM.md contract.

This validator enforces:
- required top-level fields
- non-empty values
- semantic versioning (X.Y.Z) for sbom_version
- components list structure
- component field presence and type correctness
- deterministic, structured logging for CI/CD

It does NOT enforce business logic; that lives in SBOM.md.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "sbom_version",
    "pipeline_version",
    "deployment_version",
    "components",
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


def validate_required_fields(sbom: dict):
    """Validate required fields exist and are non-empty."""
    print("[INFO] Checking required fields...")
    ok = True
    for field in REQUIRED_FIELDS:
        if field not in sbom:
            print(f"[ERROR] Missing required field: {field}")
            ok = False
        elif sbom[field] in ("", None):
            print(f"[ERROR] Field '{field}' is empty.")
            ok = False
        else:
            print(f"[OK] Field '{field}' present.")
    return ok


def validate_components(components):
    """Validate SBOM component list structure and field correctness."""
    print("[INFO] Validating SBOM components...")

    if not isinstance(components, list):
        print("[ERROR] 'components' must be a list.")
        return False

    ok = True
    for idx, comp in enumerate(components):
        prefix = f"Component #{idx+1}"

        if not isinstance(comp, dict):
            print(f"[ERROR] {prefix} is not a dict.")
            ok = False
            continue

        # Validate required component fields
        for field in ["name", "version", "source"]:
            if field not in comp or not comp[field]:
                print(f"[ERROR] {prefix} missing '{field}'.")
                ok = False
            else:
                print(f"[OK] {prefix} '{field}' present.")

        # Validate types
        if "name" in comp and not isinstance(comp["name"], str):
            print(f"[ERROR] {prefix} 'name' must be a string.")
            ok = False

        if "version" in comp and not isinstance(comp["version"], str):
            print(f"[ERROR] {prefix} 'version' must be a string.")
            ok = False

        if "source" in comp and not isinstance(comp["source"], str):
            print(f"[ERROR] {prefix} 'source' must be a string.")
            ok = False

    return ok


def main():
    parser = argparse.ArgumentParser(description="Validate SBOM JSON")
    parser.add_argument("--sbom", required=True, help="Path to SBOM JSON")
    parser.add_argument("--spec", required=True, help="Path to SBOM.md")
    args = parser.parse_args()

    sbom_path = Path(args.sbom)
    spec_path = Path(args.spec)

    if not sbom_path.exists():
        print(f"[ERROR] SBOM file not found: {sbom_path}")
        sys.exit(1)

    if not spec_path.exists():
        print(f"[ERROR] Spec file not found: {spec_path}")
        sys.exit(1)

    print("=== SBOM Validation ===")
    sbom = load_json(sbom_path)

    ok_required = validate_required_fields(sbom)
    ok_semver = validate_semver("sbom_version", sbom.get("sbom_version", ""))
    ok_components = validate_components(sbom.get("components", []))

    print("\n=== Validation Summary ===")
    if ok_required and ok_semver and ok_components:
        print("[OK] SBOM is valid.")
        sys.exit(0)
    else:
        print("[FAIL] SBOM failed validation.")
        sys.exit(2)


if __name__ == "__main__":
    main()
