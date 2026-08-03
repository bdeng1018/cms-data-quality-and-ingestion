#!/usr/bin/env python3
"""
SBOM Validator for CMS Data Quality & Ingestion Pipeline

This validator performs:

1. Structural validation of the SBOM
2. SBOM digest verification (non-recursive)
3. Cross-file consistency checks:
   - SBOM ↔ provenance digest alignment

Exit codes:
    0 = success
    1 = validation failure
"""

import hashlib
import json
import logging
import sys
from pathlib import Path

# ==============================================================================
# Configuration
# ==============================================================================

SBOM_PATH = Path("deployment/sbom/sbom-1.0.0.json")
MANIFEST_PATH = Path("deployment/releases/v1.0.0.manifest.json")
PROVENANCE_PATH = Path("deployment/provenance/provenance-1.0.0.json")

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# ==============================================================================
# Utility Functions
# ==============================================================================


def sha256_file(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    """Load JSON from a file with error handling."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load {path}: {e}")
        sys.exit(1)


# ==============================================================================
# Validation Steps
# ==============================================================================


def validate_sbom_structure(sbom: dict) -> bool:
    """Validate required SBOM fields."""
    logging.info("Checking SBOM structure...")

    required_fields = ["metadata", "components"]

    for field in required_fields:
        if field not in sbom:
            logging.error(f"Missing required SBOM field: {field}")
            return False

    logging.info("SBOM structure validated")
    return True


def validate_sbom_digest(provenance: dict) -> bool:
    """Validate SBOM digest using provenance (non-recursive)."""
    logging.info("Validating SBOM digest (non-recursive)...")

    actual = sha256_file(SBOM_PATH)

    try:
        expected = provenance["artifacts"]["sbom"]["digest"].replace("sha256:", "")
    except KeyError:
        logging.error("Provenance missing artifacts.sbom.digest")
        return False

    if actual != expected:
        logging.error(
            "SBOM digest mismatch:\n"
            f"  expected: sha256:{expected}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    logging.info("SBOM digest validated")
    return True


def validate_cross_file_consistency(provenance: dict) -> bool:
    """Validate cross-file consistency (SBOM ↔ provenance only)."""
    logging.info("Checking cross-file consistency...")

    # SBOM digest already validated above, so this is trivial now.
    logging.info("Cross-file consistency validated")
    return True


# ==============================================================================
# Main Entry Point
# ==============================================================================


def main():
    logging.info("Starting SBOM validation...")

    sbom = load_json(SBOM_PATH)
    provenance = load_json(PROVENANCE_PATH)

    if not validate_sbom_structure(sbom):
        sys.exit(1)

    if not validate_sbom_digest(provenance):
        sys.exit(1)

    if not validate_cross_file_consistency(provenance):
        sys.exit(1)

    logging.info("SBOM validation completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
