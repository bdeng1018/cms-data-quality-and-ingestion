#!/usr/bin/env python3
"""
Manifest Validator for CMS Data Quality & Ingestion Pipeline

This script validates the integrity and internal consistency of the
v1.0.0 pipeline manifest. It performs:

1. Structural validation (required fields)
2. Manifest hash verification (self-hash)
3. Cross-file consistency checks:
   - Manifest ↔ SBOM digest alignment
   - Manifest ↔ Provenance manifest digest alignment

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

MANIFEST_PATH = Path("deployment/releases/v1.0.0.manifest.json")
SBOM_PATH = Path("deployment/sbom/sbom-1.0.0.json")
PROVENANCE_PATH = Path("deployment/provenance/provenance-1.0.0.json")

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# ==============================================================================
# Utility Functions
# ==============================================================================


def sha256_file(path: Path) -> str:
    """
    Compute SHA-256 hash of a file.

    Args:
        path (Path): Path to the file.

    Returns:
        str: Hex digest of the file contents.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    """
    Load JSON from a file with error handling.

    Args:
        path (Path): Path to JSON file.

    Returns:
        dict: Parsed JSON object.

    Raises:
        SystemExit: If file cannot be loaded.
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load {path}: {e}")
        sys.exit(1)


# ==============================================================================
# Validation Steps
# ==============================================================================


def validate_manifest_structure(manifest: dict) -> bool:
    """
    Validate required top-level fields in the manifest.

    Args:
        manifest (dict): Parsed manifest JSON.

    Returns:
        bool: True if structure is valid, False otherwise.
    """
    required_fields = [
        "version",
        "release_date",
        "provenance",
        "artifacts",
        "ci_cd",
        "validation",
    ]

    logging.info("Checking manifest structure...")

    for field in required_fields:
        if field not in manifest:
            logging.error(f"Missing required field: {field}")
            return False

    logging.info("Manifest structure validated")
    return True


def validate_manifest_hash(manifest: dict, provenance: dict) -> bool:
    """
    Validate manifest hash using external provenance digest.

    The manifest no longer contains its own hash (to avoid recursion),
    so we compute the hash of the manifest file and compare it to the
    digest stored in provenance.artifacts.manifest.digest.

    Args:
        manifest (dict): Parsed manifest JSON.
        provenance (dict): Parsed provenance JSON.

    Returns:
        bool: True if hash matches, False otherwise.
    """
    logging.info("Validating manifest hash (non-recursive)...")

    # 1. Compute actual manifest hash
    actual = sha256_file(MANIFEST_PATH)

    # 2. Load expected hash from provenance
    try:
        expected = provenance["artifacts"]["manifest"]["digest"]
    except KeyError:
        logging.error("Provenance missing artifacts.manifest.digest")
        return False

    expected_clean = expected.replace("sha256:", "")

    # 3. Compare
    if actual != expected_clean:
        logging.error(
            "Manifest hash mismatch:\n"
            f"  expected: sha256:{expected_clean}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    logging.info("Manifest hash validated")
    return True


def validate_cross_file_consistency(manifest: dict, sbom: dict, provenance: dict):
    """
    Validate consistency between manifest, SBOM, and provenance.

    Args:
        manifest (dict): Manifest JSON.
        sbom (dict): SBOM JSON.
        provenance (dict): Provenance JSON.

    Returns:
        bool: True if all cross-file checks pass.
    """
    logging.info("Checking cross-file consistency...")

    # SBOM digest alignment (non-recursive)
    actual_sbom_digest = sha256_file(SBOM_PATH)

    try:
        expected_sbom_digest = provenance["artifacts"]["sbom"]["digest"].replace(
            "sha256:", ""
        )
    except KeyError:
        logging.error("Provenance missing artifacts.sbom.digest")
        return False

    if actual_sbom_digest != expected_sbom_digest:
        logging.error(
            "SBOM digest mismatch between provenance and actual SBOM file\n"
            f"  expected: sha256:{expected_sbom_digest}\n"
            f"  actual:   sha256:{actual_sbom_digest}"
        )
        return False

    logging.info("Cross-file consistency validated")
    return True


# ==============================================================================
# Main Entry Point
# ==============================================================================


def main():
    logging.info("Starting manifest validation...")

    manifest = load_json(MANIFEST_PATH)
    sbom = load_json(SBOM_PATH)
    provenance = load_json(PROVENANCE_PATH)

    if not validate_manifest_structure(manifest):
        sys.exit(1)

    if not validate_manifest_hash(manifest, provenance):
        sys.exit(1)

    if not validate_cross_file_consistency(manifest, sbom, provenance):
        sys.exit(1)

    logging.info("Manifest validation completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
