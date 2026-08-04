#!/usr/bin/env python3
"""
Version Bump Script for CMS Pipeline

Steps:
  1. Create scaffolding for a new release version.
  2. Populate placeholders inside the copied templates.
  3. Generate digests + counts.
  4. Initialize docker digest placeholder + integrity block.
  5. Ingest docker digest from CI (file-based).
  6. Finalize integrity block (self-hash + validated_at).
  7. Freeze-ready finalization (status updates).

This script produces:
  - deployment/releases/<VERSION>.manifest.json
  - deployment/sbom/sbom-<VERSION>.json
  - deployment/provenance/provenance-<VERSION>.json
"""

import datetime
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


# ==============================================================================
# Step 2: Placeholder Replacement
# ==============================================================================


def replace_placeholders(path: Path, version: str):
    text = path.read_text()

    # Basic replacements
    text = text.replace("<VERSION>", version)
    text = text.replace(
        "<ISO8601_TIMESTAMP>", datetime.datetime.utcnow().isoformat() + "Z"
    )

    # Repo-specific replacements
    text = text.replace(
        "<REPOSITORY_URL>",
        "https://github.com/bdeng1018/cms-data-quality-and-ingestion",
    )
    text = text.replace("<GHCR_NAMESPACE>", "bdeng1018")

    # Environment placeholders
    text = text.replace("<PYTHON_VERSION>", "3.11")
    text = text.replace("<DOCKER_VERSION>", "24.x")
    text = text.replace("<PYTHON_BASE_VERSION>", "3.11")

    # CI placeholders
    text = text.replace("<GITHUB_RUN_ID>", "<TO_BE_FILLED_BY_CI>")
    text = text.replace("<GITHUB_SHA>", "<TO_BE_FILLED_BY_CI>")
    text = text.replace("<GIT_REF>", "refs/heads/main")

    # Python dependency placeholders
    text = text.replace("<PANDAS_VERSION>", "2.*")
    text = text.replace("<PYYAML_VERSION>", "6.*")
    text = text.replace("<PYTEST_VERSION>", "8.*")

    # Schema placeholders
    text = text.replace("<SCHEMA_VERSION>", version)
    text = text.replace("<MANIFEST_SCHEMA_VERSION>", "0.0.0")
    text = text.replace("<DEPLOYMENT_VERSION>", version)

    path.write_text(text)
    print(f"[INFO] Populated placeholders in {path}")


def populate_all_templates(version: str):
    replace_placeholders(RELEASE_DIR / f"{version}.manifest.json", version)
    replace_placeholders(SBOM_DIR / f"sbom-{version}.json", version)
    replace_placeholders(PROV_DIR / f"provenance-{version}.json", version)


# ==============================================================================
# Step 3: Digest Generation + Count Computation
# ==============================================================================


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def update_sbom_counts(sbom_path: Path):
    sbom = json.loads(sbom_path.read_text())
    components = sbom.get("components", [])
    dependencies = sbom.get("dependencies", [])
    sbom["metadata"]["component_count"] = len(components)
    sbom["metadata"]["dependencies_count"] = len(dependencies)
    sbom_path.write_text(json.dumps(sbom, indent=4))
    print(
        f"[INFO] SBOM counts updated: {len(components)} components, {len(dependencies)} dependencies"
    )


def update_manifest_digest(manifest_path: Path):
    digest = sha256_file(manifest_path)
    manifest = json.loads(manifest_path.read_text())
    manifest["artifacts"]["manifest"]["digest"] = f"sha256:{digest}"
    manifest_path.write_text(json.dumps(manifest, indent=4))
    print(f"[INFO] Updated manifest digest: sha256:{digest}")
    return digest


def update_sbom_digest(sbom_path: Path):
    digest = sha256_file(sbom_path)
    sbom = json.loads(sbom_path.read_text())
    sbom["hash"] = f"sha256:{digest}"
    sbom["provenance"]["status"] = "pending"
    sbom_path.write_text(json.dumps(sbom, indent=4))
    print(f"[INFO] SBOM digest computed: sha256:{digest}")
    return digest


def update_provenance_digests(prov_path: Path, manifest_digest: str, sbom_digest: str):
    prov = json.loads(prov_path.read_text())
    prov["artifacts"]["manifest"]["digest"] = f"sha256:{manifest_digest}"
    prov["artifacts"]["sbom"]["digest"] = f"sha256:{sbom_digest}"
    prov_path.write_text(json.dumps(prov, indent=4))
    print("[INFO] Updated provenance digests")


# ==============================================================================
# Step 4: Docker Digest Placeholder + Integrity Block Initialization
# ==============================================================================


def initialize_docker_digest(manifest_path: Path, prov_path: Path):
    manifest = json.loads(manifest_path.read_text())
    prov = json.loads(prov_path.read_text())

    manifest["artifacts"]["docker_image"]["digest"] = "sha256:<TO_BE_FILLED_BY_CI>"
    prov["artifacts"]["docker_image"]["digest"] = "sha256:<TO_BE_FILLED_BY_CI>"

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
# Step 5: CI Docker Digest Ingestion (Option A)
# ==============================================================================


def ingest_docker_digest(manifest_path: Path, prov_path: Path):
    if not DOCKER_DIGEST_FILE.exists():
        print(
            "[WARN] No docker digest file found; CI must provide deployment/docker-digest.txt"
        )
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
# Step 6: Finalize Integrity Block (self-hash + validated_at)
# ==============================================================================


def finalize_integrity(prov_path: Path):
    prov = json.loads(prov_path.read_text())

    # Compute self-hash of provenance file
    digest = sha256_file(prov_path)
    prov["integrity"]["self_hash"] = f"sha256:{digest}"
    prov["integrity"]["validated_at"] = datetime.datetime.utcnow().isoformat() + "Z"

    prov_path.write_text(json.dumps(prov, indent=4))
    print(f"[INFO] Finalized integrity block with self-hash sha256:{digest}")


# ==============================================================================
# Step 7: Freeze-ready finalization
# ==============================================================================


def finalize_release(manifest_path: Path, sbom_path: Path, prov_path: Path):
    manifest = json.loads(manifest_path.read_text())
    sbom = json.loads(sbom_path.read_text())
    prov = json.loads(prov_path.read_text())

    manifest["validation"]["status"] = "pending"
    sbom["provenance"]["status"] = "pending"
    prov["integrity"]["validated_at"] = prov["integrity"]["validated_at"]

    manifest_path.write_text(json.dumps(manifest, indent=4))
    sbom_path.write_text(json.dumps(sbom, indent=4))
    prov_path.write_text(json.dumps(prov, indent=4))

    print("[INFO] Release finalized and ready for freeze")


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

    # Step 1: Copy templates
    copy_template(TEMPLATE_DIR / "manifest.template.json", manifest_path)
    copy_template(TEMPLATE_DIR / "sbom.template.json", sbom_path)
    copy_template(TEMPLATE_DIR / "provenance.template.json", prov_path)

    # Step 2: Populate placeholders
    populate_all_templates(version)

    # Step 3: Digests + counts
    update_sbom_counts(sbom_path)
    manifest_digest = update_manifest_digest(manifest_path)
    sbom_digest = update_sbom_digest(sbom_path)
    update_provenance_digests(prov_path, manifest_digest, sbom_digest)

    # Step 4: Initialize docker digest + integrity block
    initialize_docker_digest(manifest_path, prov_path)
    initialize_integrity_block(prov_path)

    # Step 5: Ingest docker digest from CI
    ingest_docker_digest(manifest_path, prov_path)

    # Step 6: Finalize integrity block
    finalize_integrity(prov_path)

    # Step 7: Freeze-ready finalization
    finalize_release(manifest_path, sbom_path, prov_path)

    print("[DONE] Version bump script completed successfully.")


if __name__ == "__main__":
    main()
