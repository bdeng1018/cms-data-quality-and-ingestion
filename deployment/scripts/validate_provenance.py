#!/usr/bin/env python3
"""
Provenance Validator for CMS Pipeline

Validates frozen provenance for any version:
  1. Structural validation
  2. Version alignment (provenance ↔ manifest ↔ SBOM)
  3. Manifest digest alignment
  4. SBOM digest alignment
  5. Docker digest format validation
  6. Docker digest cross-alignment (provenance ↔ manifest)
  7. Integrity block validation (including self-hash)
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

def validate_provenance_structure(prov: dict) -> bool:
    logging.info("Checking provenance structure...")

    required_fields = ["version", "generated_at", "build", "source", "artifacts", "integrity"]
    for field in required_fields:
        if field not in prov:
            logging.error(f"Missing required provenance field: {field}")
            return False

    required_artifacts = ["manifest", "sbom", "docker_image"]
    for key in required_artifacts:
        if key not in prov["artifacts"]:
            logging.error(f"Provenance missing artifacts.{key}")
            return False

    logging.info("Provenance structure validated")
    return True


def validate_version_alignment(prov: dict, manifest_path: Path, sbom_path: Path, version: str) -> bool:
    logging.info("Validating version alignment...")

    expected = version

    manifest = load_json(manifest_path)
    sbom = load_json(sbom_path)

    mv = manifest.get("version")
    sv = sbom["metadata"].get("version")
    pv = prov.get("version")

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


def validate_manifest_alignment(prov: dict, manifest_path: Path) -> bool:
    logging.info("Validating manifest digest alignment...")

    actual = sha256_file(manifest_path)

    try:
        expected = prov["artifacts"]["manifest"]["digest"].replace("sha256:", "")
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


def validate_sbom_alignment(prov: dict, sbom_path: Path) -> bool:
    logging.info("Validating SBOM digest alignment...")

    actual = sha256_file(sbom_path)

    try:
        expected = prov["artifacts"]["sbom"]["digest"].replace("sha256:", "")
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
    logging.info("Validating docker image digest format...")

    digest = prov["artifacts"]["docker_image"].get("digest")

    if not digest or not digest.startswith("sha256:"):
        logging.error("Invalid or missing docker image digest")
        return False

    logging.info("Docker digest format validated")
    return True


def validate_docker_cross_alignment(prov: dict, manifest_path: Path) -> bool:
    logging.info("Validating docker digest alignment (provenance ↔ manifest)...")

    manifest = load_json(manifest_path)

    prov_digest = prov["artifacts"]["docker_image"]["digest"]
    manifest_digest = manifest["artifacts"]["docker_image"]["digest"]

    if prov_digest != manifest_digest:
        logging.error(
            "Docker digest mismatch:\n"
            f"  provenance: {prov_digest}\n"
            f"  manifest:   {manifest_digest}"
        )
        return False

    logging.info("Docker digest aligned between provenance and manifest")
    return True


def validate_integrity_block(prov: dict, prov_path: Path) -> bool:
    logging.info("Validating integrity block...")

    integrity = prov.get("integrity", {})

    if "self_hash" not in integrity:
        logging.error("Integrity block missing self_hash")
        return False

    if not integrity["self_hash"].startswith("sha256:"):
        logging.error("Integrity self_hash must start with sha256:")
        return False

    actual = sha256_file(prov_path)
    expected = integrity["self_hash"].replace("sha256:", "")

    if actual != expected:
        logging.error(
            "Integrity self-hash mismatch:\n"
            f"  expected: sha256:{expected}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    if "validated_at" not in integrity:
        logging.error("Integrity block missing validated_at timestamp")
        return False

    logging.info("Integrity block validated")
    return True

# ==============================================================================
# Main
# ==============================================================================

def main():
    logging.info("Starting provenance validation...")

    if len(sys.argv) != 2:
        logging.error("Usage: validate_provenance.py <VERSION>")
        sys.exit(1)

    version = sys.argv[1]

    prov_path = Path(f"deployment/provenance/provenance-{version}.json")
    manifest_path = Path(f"deployment/releases/{version}.manifest.json")
    sbom_path = Path(f"deployment/sbom/sbom-{version}.json")

    prov = load_json(prov_path)

    if not validate_provenance_structure(prov):
        sys.exit(1)

    if not validate_version_alignment(prov, manifest_path, sbom_path, version):
        sys.exit(1)

    if not validate_manifest_alignment(prov, manifest_path):
        sys.exit(1)

    if not validate_sbom_alignment(prov, sbom_path):
        sys.exit(1)

    if not validate_docker_alignment(prov):
        sys.exit(1)

    if not validate_docker_cross_alignment(prov, manifest_path):
        sys.exit(1)

    if not validate_integrity_block(prov, prov_path):
        sys.exit(1)

    logging.info("Provenance validation completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
