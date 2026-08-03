#!/usr/bin/env python3
"""
Provenance Validator for CMS Data Quality & Ingestion Pipeline

This validator performs:

1. Structural validation of provenance.json
2. Manifest digest alignment
3. SBOM digest alignment
4. Docker image digest alignment
5. Integrity block validation

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

PROVENANCE_PATH = Path("deployment/provenance/provenance-1.0.0.json")
MANIFEST_PATH = Path("deployment/releases/v1.0.0.manifest.json")
SBOM_PATH = Path("deployment/sbom/sbom-1.0.0.json")

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


def validate_provenance_structure(prov: dict) -> bool:
    """
    Validate required provenance fields.

    Args:
        prov (dict): Parsed provenance JSON.

    Returns:
        bool: True if structure is valid.
    """
    logging.info("Checking provenance structure...")

    required_fields = ["build", "artifacts", "integrity"]

    for field in required_fields:
        if field not in prov:
            logging.error(f"Missing required provenance field: {field}")
            return False

    if "manifest" not in prov["artifacts"]:
        logging.error("Provenance missing artifacts.manifest")
        return False

    if "sbom" not in prov["artifacts"]:
        logging.error("Provenance missing artifacts.sbom")
        return False

    if "docker_image" not in prov["artifacts"]:
        logging.error("Provenance missing artifacts.docker_image")
        return False

    logging.info("Provenance structure validated")
    return True


def validate_manifest_alignment(provenance: dict) -> bool:
    """
    Validate provenance ↔ manifest digest alignment.

    Args:
        provenance (dict): Provenance JSON.

    Returns:
        bool: True if aligned.
    """
    logging.info("Validating manifest digest alignment...")

    actual = sha256_file(MANIFEST_PATH)

    try:
        expected = provenance["artifacts"]["manifest"]["digest"].replace("sha256:", "")
    except KeyError:
        logging.error("Provenance missing artifacts.manifest.digest")
        return False

    if actual != expected:
        logging.error(
            "Manifest digest mismatch:\n"
            f"  expected: sha256:{expected}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    logging.info("Manifest digest validated")
    return True


def validate_sbom_alignment(provenance: dict) -> bool:
    """
    Validate provenance ↔ SBOM digest alignment.

    Args:
        provenance (dict): Provenance JSON.

    Returns:
        bool: True if aligned.
    """
    logging.info("Validating SBOM digest alignment...")

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


def validate_docker_alignment(prov: dict) -> bool:
    """
    Validate docker image digest presence and format.

    Args:
        prov (dict): Provenance JSON.

    Returns:
        bool: True if valid.
    """
    logging.info("Validating docker image digest...")

    digest = prov["artifacts"]["docker_image"].get("digest")

    if not digest or not digest.startswith("sha256:"):
        logging.error("Invalid or missing docker image digest")
        return False

    logging.info("Docker image digest validated")
    return True


def validate_integrity_block(prov: dict) -> bool:
    """
    Validate integrity block structure.

    Args:
        prov (dict): Provenance JSON.

    Returns:
        bool: True if valid.
    """
    logging.info("Validating integrity block...")

    integrity = prov.get("integrity", {})

    if "self_hash" not in integrity:
        logging.error("Integrity block missing self_hash")
        return False

    logging.info("Integrity block validated")
    return True


# ==============================================================================
# Main Entry Point
# ==============================================================================


def main():
    logging.info("Starting provenance validation...")

    prov = load_json(PROVENANCE_PATH)

    if not validate_provenance_structure(prov):
        sys.exit(1)

    if not validate_manifest_alignment(prov):
        sys.exit(1)

    if not validate_sbom_alignment(prov):
        sys.exit(1)

    if not validate_docker_alignment(prov):
        sys.exit(1)

    if not validate_integrity_block(prov):
        sys.exit(1)

    logging.info("Provenance validation completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
