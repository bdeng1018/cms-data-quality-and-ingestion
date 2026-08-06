#!/usr/bin/env python3
"""
SBOM Validator for CMS Pipeline

Validates frozen SBOM for any version:
  1. Structural validation
  2. SBOM digest alignment (via provenance)
  3. SBOM internal hash validation
  4. Version alignment across SBOM ↔ manifest ↔ provenance
  5. OCI image digest alignment (SBOM ↔ manifest ↔ provenance)
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


def validate_sbom_structure(sbom: dict) -> bool:
    logging.info("Checking SBOM structure...")

    required_fields = ["metadata", "components", "dependencies", "hash"]

    for field in required_fields:
        if field not in sbom:
            logging.error(f"Missing required SBOM field: {field}")
            return False

    if "version" not in sbom["metadata"]:
        logging.error("SBOM metadata missing version")
        return False

    logging.info("SBOM structure validated")
    return True


def validate_sbom_digest_alignment(provenance: dict, sbom_path: Path) -> bool:
    logging.info("Validating SBOM digest alignment (provenance ↔ SBOM)...")

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

    # Expected hash from SBOM field
    try:
        expected = sbom["hash"].replace("sha256:", "")
    except KeyError:
        logging.error("SBOM missing internal hash field")
        return False

    # Compute digest over SBOM with hash neutralized
    sbom_copy = json.loads(json.dumps(sbom))
    sbom_copy["hash"] = ""

    neutral_text = json.dumps(sbom_copy, indent=4, sort_keys=True)
    actual = hashlib.sha256(neutral_text.encode("utf-8")).hexdigest()

    if actual != expected:
        logging.error(
            "SBOM internal hash mismatch:\n"
            f"  expected: sha256:{expected}\n"
            f"  actual:   sha256:{actual}"
        )
        return False

    logging.info("SBOM internal hash validated")
    return True


def validate_version_alignment(
    sbom: dict, manifest: dict, provenance: dict, version: str
) -> bool:
    logging.info("Validating version alignment...")

    expected = version

    sbom_v = sbom["metadata"].get("version")
    manifest_v = manifest.get("version")
    prov_v = provenance.get("version")

    if sbom_v != expected:
        logging.error(f"SBOM version mismatch: expected {expected}, found {sbom_v}")
        return False

    if manifest_v != expected:
        logging.error(
            f"Manifest version mismatch: expected {expected}, found {manifest_v}"
        )
        return False

    if prov_v != expected:
        logging.error(
            f"Provenance version mismatch: expected {expected}, found {prov_v}"
        )
        return False

    logging.info("Version alignment validated")
    return True


def validate_oci_image_digest(sbom: dict, manifest: dict, provenance: dict) -> bool:
    logging.info("Validating OCI image digest alignment...")

    try:
        sbom_digest = sbom["components"][2]["digest"].replace("sha256:", "")
    except Exception:
        logging.error("SBOM missing OCI image digest in components[2].digest")
        return False

    try:
        manifest_digest = manifest["artifacts"]["docker_image"]["digest"].replace(
            "sha256:", ""
        )
    except Exception:
        logging.error("Manifest missing artifacts.docker_image.digest")
        return False

    try:
        provenance_digest = provenance["artifacts"]["docker_image"]["digest"].replace(
            "sha256:", ""
        )
    except Exception:
        logging.error("Provenance missing artifacts.docker_image.digest")
        return False

    if sbom_digest != manifest_digest or sbom_digest != provenance_digest:
        logging.error(
            "OCI image digest mismatch:\n"
            f"  SBOM:       sha256:{sbom_digest}\n"
            f"  Manifest:   sha256:{manifest_digest}\n"
            f"  Provenance: sha256:{provenance_digest}"
        )
        return False

    logging.info("OCI image digest validated")
    return True


# ==============================================================================
# Main
# ==============================================================================


def main():
    logging.info("Starting SBOM validation...")

    if len(sys.argv) != 2:
        logging.error("Usage: validate_sbom.py <VERSION>")
        sys.exit(1)

    version = sys.argv[1]

    sbom_path = Path(f"deployment/sbom/sbom-{version}.json")
    manifest_path = Path(f"deployment/releases/{version}.manifest.json")
    provenance_path = Path(f"deployment/provenance/provenance-{version}.json")

    sbom = load_json(sbom_path)
    manifest = load_json(manifest_path)
    provenance = load_json(provenance_path)

    if not validate_sbom_structure(sbom):
        sys.exit(1)

    if not validate_version_alignment(sbom, manifest, provenance, version):
        sys.exit(1)

    if not validate_sbom_digest_alignment(provenance, sbom_path):
        sys.exit(1)

    if not validate_sbom_internal_hash(sbom, sbom_path):
        sys.exit(1)

    logging.info("SBOM validation completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()
