#!/usr/bin/env python3
"""
Manifest Validator for CMS Pipeline

Validates frozen manifest for any version:
  1. Structural validation
  2. Version alignment across manifest, SBOM, provenance
  3. Manifest digest alignment (via provenance)
  4. SBOM digest alignment (via provenance)
  5. SBOM internal hash validation
  6. Docker digest alignment (manifest ↔ provenance)
  7. Provenance digest alignment (manifest ↔ provenance)
  8. Provenance self-hash validation
"""

import hashlib
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# ==============================================================================
# Utility Functions
# ==============================================================================

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path):
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
    logging.info("Checking manifest structure...")

    required_fields = [
        "version",
        "schema_version",
        "generated_at",
        "artifacts",
        "metadata",
        "validation",
    ]

    for field in required_fields:
        if field not in manifest:
            logging.error(f"Missing required field: {field}")
            return False

    required_artifacts = ["manifest", "sbom", "docker_image", "provenance"]
    for key in required_artifacts:
        if key not in manifest["artifacts"]:
            logging.error(f"Manifest missing artifacts.{key}")
            return False

    if "status" not in manifest["validation"]:
        logging.error("Manifest missing validation.status")
        return False

    logging.info("Manifest structure validated")
    return True


def validate_version_alignment(manifest: dict, sbom: dict, provenance: dict, version: str) -> bool:
    logging.info("Validating version alignment...")

    mv = manifest.get("version")
    sv = sbom["metadata"].get("version")
    pv = provenance.get("version")

    expected = version

    if mv != expected:
        logging.error(f"Manifest version mismatch: expected {expected}, found {mv}")
        return False

    if sv != expected:
        logging.error(f"SBOM version mismatch: expected {expected}, found {sv}")
        return False

    if pv != expected:
        logging.error(f"Provenance version mismatch: expected {expected}, found {pv}")
        return False

    logging.info("Version alignment validated")
    return True


def validate_manifest_hash(manifest: dict, provenance: dict, manifest_path: Path) -> bool:
    logging.info("Validating manifest digest alignment...")

    actual = sha256_file(manifest_path)

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


def validate_sbom_alignment(provenance: dict, sbom_path: Path) -> bool:
    logging.info("Validating SBOM digest alignment...")

    actual = sha256_file(sbom_path)

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


def validate_sbom_internal_hash(sbom: dict, sbom_path: Path) -> bool:
    logging.info("Validating SBOM internal hash...")

    actual = sha256_file(sbom_path)

    try:
        expected = sbom["hash"].replace("sha256:", "")
    except KeyError:
        logging.error("SBOM missing internal hash field")
        return False

    if actual != expected:
        logging.error(
            "SBOM internal hash mismatch:\n"
            f"  expected: sha256:{expected}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    logging.info("SBOM internal hash validated")
    return True


def validate_docker_alignment(manifest: dict, provenance: dict) -> bool:
    logging.info("Validating docker digest alignment...")

    try:
        manifest_digest = manifest["artifacts"]["docker_image"]["digest"]
        provenance_digest = provenance["artifacts"]["docker_image"]["digest"]
    except KeyError:
        logging.error("Missing docker_image.digest in manifest or provenance")
        return False

    if manifest_digest != provenance_digest:
        logging.error(
            "Docker digest mismatch:\n"
            f"  manifest:   {manifest_digest}\n"
            f"  provenance: {provenance_digest}"
        )
        return False

    logging.info("Docker digest validated")
    return True


def validate_provenance_alignment(manifest: dict, provenance: dict, provenance_path: Path) -> bool:
    logging.info("Validating provenance digest alignment...")

    actual = sha256_file(provenance_path)

    try:
        expected = manifest["artifacts"]["provenance"]["digest"].replace("sha256:", "")
    except KeyError:
        logging.error("Manifest missing artifacts.provenance.digest")
        return False

    if actual != expected:
        logging.error(
            "Provenance digest mismatch:\n"
            f"  expected: sha256:{expected}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    logging.info("Provenance digest validated")
    return True


def validate_provenance_self_hash(provenance: dict, provenance_path: Path) -> bool:
    logging.info("Validating provenance self-hash...")

    actual = sha256_file(provenance_path)

    try:
        expected = provenance["integrity"]["self_hash"].replace("sha256:", "")
    except KeyError:
        logging.error("Provenance missing integrity.self_hash")
        return False

    if actual != expected:
        logging.error(
            "Provenance self-hash mismatch:\n"
            f"  expected: sha256:{expected}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    logging.info("Provenance self-hash validated")
    return True

# ==============================================================================
# Main
# ==============================================================================

def main():
    logging.info("Starting manifest validation...")

    if len(sys.argv) != 2:
        logging.error("Usage: validate_manifest.py <VERSION>")
        sys.exit(1)

    version = sys.argv[1]

    manifest_path = Path(f"deployment/releases/{version}.manifest.json")
    sbom_path = Path(f"deployment/sbom/sbom-{version}.json")
    provenance_path = Path(f"deployment/provenance/provenance-{version}.json")

    manifest = load_json(manifest_path)
    sbom = load_json(sbom_path)
    provenance = load_json(provenance_path)

    if not validate_manifest_structure(manifest):
        sys.exit(1)

    if not validate_version_alignment(manifest, sbom, provenance, version):
        sys.exit(1)

    if not validate_manifest_hash(manifest, provenance, manifest_path):
        sys.exit(1)

    if not validate_sbom_alignment(provenance, sbom_path):
        sys.exit(1)

    if not validate_sbom_internal_hash(sbom, sbom_path):
        sys.exit(1)

    if not validate_docker_alignment(manifest, provenance):
        sys.exit(1)

    if not validate_provenance_alignment(manifest, provenance, provenance_path):
        sys.exit(1)

    if not validate_provenance_self_hash(provenance, provenance_path):
        sys.exit(1)

    logging.info("Manifest validation completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
