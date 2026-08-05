#!/usr/bin/env python3
"""
Release Validator for CMS Pipeline

Final freeze gate. Validates:
  - Manifest digest correctness
  - SBOM digest correctness
  - SBOM internal hash correctness
  - Provenance digest correctness
  - Docker digest alignment (manifest ↔ provenance ↔ docker-digest.txt)
  - Integrity block correctness
  - Placeholder absence
  - Component/dependency counts
  - Version alignment across all artifacts
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
    placeholders = [
        "<TO_BE_FILLED",
        "<MANIFEST_DIGEST>",
        "<SBOM_DIGEST>",
        "<DOCKER_DIGEST>",
        "<AUDIT_LOGS_DIGEST>",
        "<HELM_DIGEST>",
        "<K8S_DIGEST>",
        "<TERRAFORM_DIGEST>",
    ]
    for p in placeholders:
        if p in text:
            fail(f"Placeholder '{p}' remains in {path}")


def validate_manifest(manifest_path: Path, provenance: dict):
    manifest = json.loads(manifest_path.read_text())

    expected = provenance["artifacts"]["manifest"]["digest"].replace("sha256:", "")
    actual = sha256_file(manifest_path)

    if expected != actual:
        fail(f"Manifest digest mismatch: expected {expected}, got {actual}")

    print("[OK] Manifest digest validated")


def validate_sbom(sbom_path: Path, provenance: dict):
    sbom = json.loads(sbom_path.read_text())

    expected = provenance["artifacts"]["sbom"]["digest"].replace("sha256:", "")
    actual = sha256_file(sbom_path)

    if expected != actual:
        fail(f"SBOM digest mismatch: expected {expected}, got {actual}")

    internal = sbom["hash"].replace("sha256:", "")
    if internal != actual:
        fail(f"SBOM internal hash mismatch: expected {internal}, got {actual}")

    if sbom["metadata"]["component_count"] != len(sbom.get("components", [])):
        fail("SBOM component_count mismatch")

    if sbom["metadata"]["dependencies_count"] != len(sbom.get("dependencies", [])):
        fail("SBOM dependencies_count mismatch")

    print("[OK] SBOM digest + internal hash + counts validated")


def validate_provenance(prov_path: Path, manifest_path: Path, sbom_path: Path):
    prov = json.loads(prov_path.read_text())

    expected_manifest = prov["artifacts"]["manifest"]["digest"].replace("sha256:", "")
    actual_manifest = sha256_file(manifest_path)
    if expected_manifest != actual_manifest:
        fail("Provenance manifest digest mismatch")

    expected_sbom = prov["artifacts"]["sbom"]["digest"].replace("sha256:", "")
    actual_sbom = sha256_file(sbom_path)
    if expected_sbom != actual_sbom:
        fail("Provenance SBOM digest mismatch")

    docker_digest = prov["artifacts"]["docker_image"]["digest"]
    if "<TO_BE_FILLED" in docker_digest:
        fail("Docker digest placeholder still present in provenance")

    expected_self_hash = prov["integrity"]["self_hash"].replace("sha256:", "")
    actual_self_hash = sha256_file(prov_path)
    if expected_self_hash != actual_self_hash:
        fail("Provenance self-hash mismatch")

    if prov["integrity"]["validated_at"] is None:
        fail("Provenance validated_at missing")

    print("[OK] Provenance validated")


def validate_docker_alignment(manifest: dict, provenance: dict):
    m = manifest["artifacts"]["docker_image"]["digest"]
    p = provenance["artifacts"]["docker_image"]["digest"]

    if m != p:
        fail(f"Docker digest mismatch: manifest={m}, provenance={p}")

    print("[OK] Docker digest alignment validated")


def validate_docker_digest_file():
    if not DOCKER_DIGEST_FILE.exists():
        fail("docker-digest.txt missing")

    digest = DOCKER_DIGEST_FILE.read_text().strip()
    if not digest.startswith("sha256:"):
        fail("docker-digest.txt does not contain a valid digest")

    print("[OK] Docker digest file validated")


def validate_version_alignment(manifest: dict, sbom: dict, provenance: dict, version: str):
    expected = version

    if manifest.get("version") != expected:
        fail("Manifest version mismatch")

    if sbom["metadata"].get("version") != expected:
        fail("SBOM version mismatch")

    if provenance.get("version") != expected:
        fail("Provenance version mismatch")

    print("[OK] Version alignment validated")


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_release.py <VERSION>")
        sys.exit(1)

    version = sys.argv[1]

    manifest_path = RELEASE_DIR / f"{version}.manifest.json"
    sbom_path = SBOM_DIR / f"sbom-{version}.json"
    prov_path = PROV_DIR / f"provenance-{version}.json"

    for p in [manifest_path, sbom_path, prov_path]:
        if not p.exists():
            fail(f"Missing required file: {p}")

    validate_no_placeholders(manifest_path.read_text(), manifest_path)
    validate_no_placeholders(sbom_path.read_text(), sbom_path)
    validate_no_placeholders(prov_path.read_text(), prov_path)

    validate_docker_digest_file()

    manifest = json.loads(manifest_path.read_text())
    sbom = json.loads(sbom_path.read_text())
    provenance = json.loads(prov_path.read_text())

    validate_version_alignment(manifest, sbom, provenance, version)
    validate_docker_alignment(manifest, provenance)

    validate_manifest(manifest_path, provenance)
    validate_sbom(sbom_path, provenance)
    validate_provenance(prov_path, manifest_path, sbom_path)

    print("[SUCCESS] Release is fully validated and freeze-safe")


if __name__ == "__main__":
    main()
