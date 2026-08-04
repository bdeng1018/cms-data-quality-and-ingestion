#!/usr/bin/env python3
"""
Release Validator for CMS Pipeline

Validates:
  - Manifest digest correctness
  - SBOM digest correctness
  - Provenance digest correctness
  - Docker digest presence
  - Integrity block correctness
  - Placeholder absence
  - Component/dependency counts
  - Cross-file alignment

This is the final freeze gate before tagging a release.
"""

import hashlib
import json
import sys
from pathlib import Path

RELEASE_DIR = Path("deployment/releases")
SBOM_DIR = Path("deployment/sbom")
PROV_DIR = Path("deployment/provenance")
DOCKER_DIGEST_FILE = Path("deployment/docker-digest.txt")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str):
    print(f"[ERROR] {msg}")
    sys.exit(1)


def validate_no_placeholders(text: str, path: Path):
    if "<TO_BE_FILLED" in text or "<VERSION>" in text:
        fail(f"Placeholders remain in {path}")


def validate_manifest(manifest_path: Path):
    manifest = json.loads(manifest_path.read_text())
    digest_expected = manifest["artifacts"]["manifest"]["digest"].replace("sha256:", "")
    digest_actual = sha256_file(manifest_path)

    if digest_expected != digest_actual:
        fail(f"Manifest digest mismatch: expected {digest_expected}, got {digest_actual}")

    print("[OK] Manifest digest validated")


def validate_sbom(sbom_path: Path):
    sbom = json.loads(sbom_path.read_text())
    digest_expected = sbom["hash"].replace("sha256:", "")
    digest_actual = sha256_file(sbom_path)

    if digest_expected != digest_actual:
        fail(f"SBOM digest mismatch: expected {digest_expected}, got {digest_actual}")

    # Count validation
    components = sbom.get("components", [])
    dependencies = sbom.get("dependencies", [])
    if sbom["metadata"]["component_count"] != len(components):
        fail("SBOM component_count mismatch")

    if sbom["metadata"]["dependencies_count"] != len(dependencies):
        fail("SBOM dependencies_count mismatch")

    print("[OK] SBOM digest + counts validated")


def validate_provenance(prov_path: Path):
    prov = json.loads(prov_path.read_text())

    # Validate manifest digest alignment
    manifest_digest = prov["artifacts"]["manifest"]["digest"].replace("sha256:", "")
    manifest_path = RELEASE_DIR / f"{prov['pipeline_version']}.manifest.json"
    manifest_actual = sha256_file(manifest_path)
    if manifest_digest != manifest_actual:
        fail("Provenance manifest digest mismatch")

    # Validate SBOM digest alignment
    sbom_digest = prov["artifacts"]["sbom"]["digest"].replace("sha256:", "")
    sbom_path = SBOM_DIR / f"sbom-{prov['pipeline_version']}.json"
    sbom_actual = sha256_file(sbom_path)
    if sbom_digest != sbom_actual:
        fail("Provenance SBOM digest mismatch")

    # Validate docker digest presence
    docker_digest = prov["artifacts"]["docker_image"]["digest"]
    if "<TO_BE_FILLED" in docker_digest:
        fail("Docker digest placeholder still present in provenance")

    # Validate integrity block
    self_hash_expected = prov["integrity"]["self_hash"].replace("sha256:", "")
    self_hash_actual = sha256_file(prov_path)
    if self_hash_expected != self_hash_actual:
        fail("Provenance self-hash mismatch")

    if prov["integrity"]["validated_at"] is None:
        fail("Provenance validated_at missing")

    print("[OK] Provenance validated")


def validate_docker_digest():
    if not DOCKER_DIGEST_FILE.exists():
        fail("docker-digest.txt missing")

    digest = DOCKER_DIGEST_FILE.read_text().strip()
    if not digest.startswith("sha256:"):
        fail("docker-digest.txt does not contain a valid digest")

    print("[OK] Docker digest file validated")


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_release.py <VERSION>")
        sys.exit(1)

    version = sys.argv[1]

    manifest_path = RELEASE_DIR / f"{version}.manifest.json"
    sbom_path = SBOM_DIR / f"sbom-{version}.json"
    prov_path = PROV_DIR / f"provenance-{version}.json"

    # Check files exist
    for p in [manifest_path, sbom_path, prov_path]:
        if not p.exists():
            fail(f"Missing required file: {p}")

    # Check placeholders
    validate_no_placeholders(manifest_path.read_text(), manifest_path)
    validate_no_placeholders(sbom_path.read_text(), sbom_path)
    validate_no_placeholders(prov_path.read_text(), prov_path)

    # Validate docker digest file
    validate_docker_digest()

    # Validate each artifact
    validate_manifest(manifest_path)
    validate_sbom(sbom_path)
    validate_provenance(prov_path)

    print("[SUCCESS] Release is fully validated and freeze-safe")


if __name__ == "__main__":
    main()
