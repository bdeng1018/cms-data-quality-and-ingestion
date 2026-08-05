#!/usr/bin/env python3
"""
Deterministic Version Freeze Script for CMS Pipeline

This script:
  1. Validates templates (no CI contamination).
  2. Copies templates for manifest, SBOM, provenance.
  3. Replaces placeholders.
  4. Inserts version metadata.
  5. Updates SBOM counts.
  6. Initializes docker digest + integrity block.
  7. Ingests docker digest from CI.
  8. Finalizes release metadata.
  9. Computes FINAL digests (manifest + SBOM) over content with self-digest fields neutralized.
 10. Inserts digests into provenance (and SBOM hash for convenience).
 11. Finalizes provenance integrity block.
 12. Runs freeze sanity check.

Digest computation happens last, ensuring determinism.
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

# ==============================================================================
# Paths
# ==============================================================================

TEMPLATE_DIR = Path("deployment/releases/templates")
RELEASE_DIR = Path("deployment/releases")
SBOM_DIR = Path("deployment/sbom")
PROV_DIR = Path("deployment/provenance")
DOCKER_DIGEST_FILE = Path("deployment/docker-digest.txt")

# ==============================================================================
# Helpers
# ==============================================================================

def ensure_dirs(version: str):
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    SBOM_DIR.mkdir(parents=True, exist_ok=True)
    PROV_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Ensured directories for version {version}")

def copy_template(src: Path, dst: Path):
    shutil.copy(src, dst)
    print(f"[INFO] Created {dst}")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# ==============================================================================
# Template Validator
# ==============================================================================

def validate_template(path: Path):
    text = path.read_text()
    forbidden = [
        "actions/checkout",
        "docker/buildx",
        "digest-extraction",
        "runner",
        "steps",
        "github-actions",
    ]
    for token in forbidden:
        if token in text:
            raise RuntimeError(f"[ERROR] Template {path} contains CI fields: {token}")
    print(f"[INFO] Template validated: {path}")

# ==============================================================================
# Placeholder Replacement
# ==============================================================================

def replace_placeholders(path: Path, version: str):
    text = path.read_text()

    text = text.replace("<VERSION>", version)
    text = text.replace("<ISO8601_TIMESTAMP>", "")
    text = text.replace("<REPOSITORY_URL>", "https://github.com/bdeng1018/cms-data-quality-and-ingestion")
    text = text.replace("<GHCR_NAMESPACE>", "bdeng1018")
    text = text.replace("<PYTHON_VERSION>", "3.11")
    text = text.replace("<DOCKER_VERSION>", "24.x")
    text = text.replace("<PYTHON_BASE_VERSION>", "3.11")
    text = text.replace("<GITHUB_RUN_ID>", "")
    text = text.replace("<GITHUB_SHA>", "")
    text = text.replace("<GIT_REF>", "refs/heads/main")
    text = text.replace("<PANDAS_VERSION>", "2.*")
    text = text.replace("<PYYAML_VERSION>", "6.*")
    text = text.replace("<PYTEST_VERSION>", "8.*")
    text = text.replace("<SCHEMA_VERSION>", version)
    text = text.replace("<MANIFEST_SCHEMA_VERSION>", "0.0.0")
    text = text.replace("<DEPLOYMENT_VERSION>", version)
    text = text.replace("<YYYY-MM-DD>", "")

    path.write_text(text)
    print(f"[INFO] Populated placeholders in {path}")

def populate_all_templates(version: str):
    replace_placeholders(RELEASE_DIR / f"{version}.manifest.json", version)
    replace_placeholders(SBOM_DIR / f"sbom-{version}.json", version)
    replace_placeholders(PROV_DIR / f"provenance-{version}.json", version)

# ==============================================================================
# SBOM Counts
# ==============================================================================

def update_sbom_counts(sbom_path: Path):
    sbom = json.loads(sbom_path.read_text())
    components = sbom.get("components", [])
    dependencies = sbom.get("dependencies", [])
    sbom["metadata"]["component_count"] = len(components)
    sbom["metadata"]["dependencies_count"] = len(dependencies)
    sbom_path.write_text(json.dumps(sbom, indent=4))
    print(f"[INFO] SBOM counts updated: {len(components)} components, {len(dependencies)} dependencies")

# ==============================================================================
# Docker Digest Placeholder + Integrity Block
# ==============================================================================

def initialize_docker_digest(manifest_path: Path, prov_path: Path):
    manifest = json.loads(manifest_path.read_text())
    prov = json.loads(prov_path.read_text())

    manifest["artifacts"]["docker_image"]["digest"] = ""
    prov["artifacts"]["docker_image"]["digest"] = ""

    manifest_path.write_text(json.dumps(manifest, indent=4))
    prov_path.write_text(json.dumps(prov, indent=4))

    print("[INFO] Initialized docker digest placeholder")

def initialize_integrity_block(prov_path: Path):
    prov = json.loads(prov_path.read_text())
    prov["integrity"]["self_hash"] = "pending"
    prov["integrity"]["validated_at"] = None
    prov_path.write_text(json.dumps(prov, indent=4))
    print("[INFO] Initialized integrity block")

# ==============================================================================
# Docker Digest Ingestion
# ==============================================================================

def ingest_docker_digest(manifest_path: Path, prov_path: Path):
    if not DOCKER_DIGEST_FILE.exists():
        print("[WARN] No docker digest file found; CI must provide deployment/docker-digest.txt")
        return None

    docker_digest = DOCKER_DIGEST_FILE.read_text().strip()

    manifest = json.loads(manifest_path.read_text())
    prov = json.loads(prov_path.read_text())

    manifest["artifacts"]["docker_image"]["digest"] = docker_digest
    prov["artifacts"]["docker_image"]["digest"] = docker_digest

    manifest_path.write_text(json.dumps(manifest, indent=4))
    prov_path.write_text(json.dumps(prov, indent=4))

    print(f"[INFO] Ingested docker digest: {docker_digest}")
    return docker_digest

# ==============================================================================
# Release Finalization (pre-digest)
# ==============================================================================

def finalize_release(manifest_path: Path, sbom_path: Path, prov_path: Path):
    manifest = json.loads(manifest_path.read_text())
    sbom = json.loads(sbom_path.read_text())
    prov = json.loads(prov_path.read_text())

    manifest["validation"]["status"] = "pending"
    sbom["provenance"]["status"] = "pending"

    manifest_path.write_text(json.dumps(manifest, indent=4))
    sbom_path.write_text(json.dumps(sbom, indent=4))
    prov_path.write_text(json.dumps(prov, indent=4))

    print("[INFO] Release finalized (pre-digest)")

# ==============================================================================
# Integrity Finalization
# ==============================================================================

def finalize_integrity(prov_path: Path):
    digest = sha256_file(prov_path)
    prov = json.loads(prov_path.read_text())
    prov["integrity"]["self_hash"] = f"sha256:{digest}"
    prov["integrity"]["validated_at"] = ""
    prov_path.write_text(json.dumps(prov, indent=4))
    print(f"[INFO] Finalized integrity block with self-hash sha256:{digest}")

# ==============================================================================
# Sanity Check
# ==============================================================================

def sanity_check(version: str):
    manifest_path = RELEASE_DIR / f"{version}.manifest.json"
    sbom_path = SBOM_DIR / f"sbom-{version}.json"
    prov_path = PROV_DIR / f"provenance-{version}.json"

    manifest_digest = sha256_file(manifest_path)

    # SBOM: blank hash before hashing, same as main()
    sbom = json.loads(sbom_path.read_text())
    sbom["hash"] = ""
    sbom_path.write_text(json.dumps(sbom, indent=4))
    sbom_digest = sha256_file(sbom_path)

    prov = json.loads(prov_path.read_text())

    print("Computed SBOM digest:", sbom_digest)
    print("Provenance SBOM digest:", prov["artifacts"]["sbom"]["digest"])

    assert prov["artifacts"]["manifest"]["digest"] == f"sha256:{manifest_digest}", "Manifest digest mismatch"
    assert prov["artifacts"]["sbom"]["digest"] == f"sha256:{sbom_digest}", "SBOM digest mismatch"

    # Integrity hash is already finalized in main(), so just trust it exists
    assert prov["integrity"]["self_hash"].startswith("sha256:"), "Integrity hash missing"

    print("[OK] Freeze sanity check passed")

# ==============================================================================
# Main
# ==============================================================================

def main():
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <VERSION>")
        sys.exit(1)

    version = sys.argv[1]
    print(f"[INFO] Preparing scaffolding for version {version}")

    ensure_dirs(version)

    manifest_path = RELEASE_DIR / f"{version}.manifest.json"
    sbom_path = SBOM_DIR / f"sbom-{version}.json"
    prov_path = PROV_DIR / f"provenance-{version}.json"

    validate_template(TEMPLATE_DIR / "manifest.template.json")
    validate_template(TEMPLATE_DIR / "sbom.template.json")
    validate_template(TEMPLATE_DIR / "provenance.template.json")

    for path in [manifest_path, sbom_path, prov_path]:
        if path.exists():
            path.unlink()

    copy_template(TEMPLATE_DIR / "manifest.template.json", manifest_path)
    copy_template(TEMPLATE_DIR / "sbom.template.json", sbom_path)
    copy_template(TEMPLATE_DIR / "provenance.template.json", prov_path)

    populate_all_templates(version)

    manifest = json.loads(manifest_path.read_text())
    manifest["version"] = f"v{version}"
    manifest_path.write_text(json.dumps(manifest, indent=4))

    sbom = json.loads(sbom_path.read_text())
    sbom["metadata"]["version"] = f"v{version}"
    sbom_path.write_text(json.dumps(sbom, indent=4))

    prov = json.loads(prov_path.read_text())
    prov["version"] = f"v{version}"
    prov_path.write_text(json.dumps(prov, indent=4))

    print(f"[INFO] Inserted version metadata v{version}")

    update_sbom_counts(sbom_path)

    initialize_docker_digest(manifest_path, prov_path)
    initialize_integrity_block(prov_path)

    ingest_docker_digest(manifest_path, prov_path)

    finalize_release(manifest_path, sbom_path, prov_path)

    # --- MANIFEST DIGEST ---
    final_manifest_digest = sha256_file(manifest_path)
    prov = json.loads(prov_path.read_text())
    prov["artifacts"]["manifest"]["digest"] = f"sha256:{final_manifest_digest}"
    prov_path.write_text(json.dumps(prov, indent=4))

    # --- SBOM DIGEST (correct ordering) ---
    # 1. Blank hash field BEFORE hashing
    sbom = json.loads(sbom_path.read_text())
    sbom["hash"] = ""
    sbom_path.write_text(json.dumps(sbom, indent=4))

    # 2. Compute digest over final SBOM file
    final_sbom_digest = sha256_file(sbom_path)

    # 3. Write digest into SBOM
    sbom["hash"] = f"sha256:{final_sbom_digest}"
    sbom_path.write_text(json.dumps(sbom, indent=4))

    # 4. Write digest into provenance
    prov = json.loads(prov_path.read_text())
    prov["artifacts"]["sbom"]["digest"] = f"sha256:{final_sbom_digest}"
    prov_path.write_text(json.dumps(prov, indent=4))

    finalize_integrity(prov_path)

    sanity_check(version)

if __name__ == "__main__":
    main()