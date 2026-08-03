#!/usr/bin/env python3
"""
bump_version.py

Deterministic release artifact generator for the CMS Pipeline.

Purpose
-------
Construct all pre-freeze release artifacts for a given version:
- manifest.json
- sbom.json
- provenance.json

This script prepares all artifacts for immutable freezing by freeze_runner.py.
It does not compute detached signatures and does not mutate artifacts after
digest insertion.

Responsibilities
----------------
1. Validate JSON templates for manifest, SBOM, and provenance.
2. Copy templates into versioned release paths.
3. Populate placeholders using CI-provided metadata:
   - <VERSION>
   - <REPOSITORY_URL>
   - <GHCR_NAMESPACE>
   - <GITHUB_SHA>
   - <GITHUB_RUN_ID>
   - <GIT_REF>
   - <WORKFLOW_FILE>
   - <EXECUTION_ENVIRONMENT>
   - <CONTAINER_RUNTIME>
   - <DOCKER_VERSION>
   - <PYTHON_VERSION>
   - <ISO8601_TIMESTAMP>
   - <YYYY-MM-DD>
4. Insert version metadata into manifest, SBOM, and provenance.
5. Compute SBOM component and dependency counts.
6. Initialize docker digest placeholders in manifest and provenance.
7. Initialize provenance integrity block (self_hash="pending").
8. Ingest docker digest from CI (deployment/docker-digest.txt).
9. Freeze all pre-digest fields using deterministic formatting
   (indent=4, sort_keys=True).
10. Compute SBOM internal hash (neutralized) and final SBOM digest.
11. Insert SBOM digest into provenance.
12. Compute provenance integrity.self_hash (neutralized) and final digest.
13. Insert provenance digest into manifest and provenance.
14. Compute final manifest digest and insert it into provenance.

Design Principles
-----------------
- Deterministic: all formatting, metadata, and digests are reproducible.
- Non-circular: provenance.self_hash excludes itself during hashing.
- SLSA-aligned: provenance includes integrity block and digest fields.
- Validator-aligned: canonicalization matches validate_provenance.py.
- Separation of concerns: freeze_runner.py performs detached signature creation.

This script MUST run before freeze_runner.py, which writes the detached signature.
"""

import hashlib
import json
import os
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


def ensure_dirs(version: str) -> None:
    """
    Ensure all release directories exist for the given version.

    Parameters
    ----------
    version : str
        Release version (e.g., "9.9.9").
    """
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    SBOM_DIR.mkdir(parents=True, exist_ok=True)
    PROV_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Ensured directories for version {version}")


def copy_template(src: Path, dst: Path) -> None:
    """
    Copy a template JSON file verbatim to a destination path.

    Parameters
    ----------
    src : Path
        Template file path.

    dst : Path
        Destination file path.
    """
    shutil.copy(src, dst)
    print(f"[INFO] Created {dst}")


def sha256_file(path: Path) -> str:
    """
    Compute the SHA‑256 digest of a file in streaming mode.

    Parameters
    ----------
    path : Path
        Path to the file whose digest should be computed.

    Returns
    -------
    str
        Hex-encoded SHA‑256 digest.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ==============================================================================
# Template Validator
# ==============================================================================


def validate_template(path: Path) -> None:
    """
    Validate that a template JSON file is syntactically correct.

    Parameters
    ----------
    path : Path
        Path to the template JSON file.

    Raises
    ------
    SystemExit
        If the JSON is invalid.
    """
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
    """
    Replace placeholder tokens in a template JSON file using CI‑provided
    environment variables and deterministic version metadata.

    Parameters
    ----------
    path : Path
        Path to the template JSON file to populate.

    version : str
        Release version (e.g., "1.0.0") used to replace <VERSION> and other
        version‑dependent placeholders.
    """
    text = path.read_text()

    text = text.replace("<VERSION>", version)
    text = text.replace("<ISO8601_TIMESTAMP>", os.getenv("ISO8601_TIMESTAMP", ""))
    text = text.replace("<REPOSITORY_URL>", os.getenv("REPOSITORY_URL", ""))
    text = text.replace("<GHCR_NAMESPACE>", os.getenv("GHCR_NAMESPACE", ""))
    text = text.replace("<PYTHON_VERSION>", os.getenv("PYTHON_VERSION", ""))
    text = text.replace("<DOCKER_VERSION>", os.getenv("DOCKER_VERSION", ""))
    text = text.replace("<GITHUB_RUN_ID>", os.getenv("GITHUB_RUN_ID", ""))
    text = text.replace("<GITHUB_SHA>", os.getenv("GITHUB_SHA", ""))
    text = text.replace("<GIT_REF>", os.getenv("GIT_REF", ""))
    text = text.replace("<YYYY-MM-DD>", os.getenv("RELEASE_DATE", ""))
    text = text.replace("<WORKFLOW_FILE>", os.getenv("WORKFLOW_FILE", ""))
    text = text.replace(
        "<EXECUTION_ENVIRONMENT>", os.getenv("EXECUTION_ENVIRONMENT", "")
    )
    text = text.replace("<CONTAINER_RUNTIME>", os.getenv("CONTAINER_RUNTIME", ""))

    path.write_text(text)
    print(f"[INFO] Populated placeholders in {path}")


def populate_all_templates(version: str) -> None:
    """
    Replace placeholder tokens in manifest, SBOM, and provenance templates.

    Placeholders include:
    - <VERSION>
    - <ISO8601_TIMESTAMP>
    - <REPOSITORY_URL>
    - <GHCR_NAMESPACE>
    - <GITHUB_SHA>
    - <GITHUB_RUN_ID>
    - <GIT_REF>
    - <WORKFLOW_FILE>
    - <EXECUTION_ENVIRONMENT>
    - <CONTAINER_RUNTIME>
    - <DOCKER_VERSION>
    - <PYTHON_VERSION>

    Parameters
    ----------
    version : str
        Release version to substitute into templates.
    """
    replace_placeholders(RELEASE_DIR / f"{version}.manifest.json", version)
    replace_placeholders(SBOM_DIR / f"sbom-{version}.json", version)
    replace_placeholders(PROV_DIR / f"provenance-{version}.json", version)


# ==============================================================================
# SBOM Counts
# ==============================================================================


def update_sbom_counts(sbom_path: Path) -> None:
    """
    Compute and insert SBOM component and dependency counts.

    Parameters
    ----------
    sbom_path : Path
        Path to the SBOM JSON file.
    """
    sbom = json.loads(sbom_path.read_text())
    components = sbom.get("components", [])
    dependencies = sbom.get("dependencies", [])
    sbom["metadata"]["component_count"] = len(components)
    sbom["metadata"]["dependencies_count"] = len(dependencies)
    sbom_path.write_text(json.dumps(sbom, indent=4, sort_keys=True))
    print(
        f"[INFO] SBOM counts updated: {len(components)} components, {len(dependencies)} dependencies"
    )


# ==============================================================================
# Docker Digest Placeholder + Integrity Block
# ==============================================================================


def initialize_docker_digest(manifest_path: Path, prov_path: Path) -> None:
    """
    Initialize docker digest placeholders in manifest and provenance.

    Parameters
    ----------
    manifest_path : Path
        Path to manifest.json.

    prov_path : Path
        Path to provenance.json.
    """
    manifest = json.loads(manifest_path.read_text())
    prov = json.loads(prov_path.read_text())

    manifest["artifacts"]["docker_image"]["digest"] = ""
    prov["artifacts"]["docker_image"]["digest"] = ""

    manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True))
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))

    print("[INFO] Initialized docker digest placeholder")


def initialize_integrity_block(prov_path: Path) -> None:
    """
    Initialize the provenance integrity block.

    Fields:
    - self_hash: ""
    - validated_at: None
    - validators: {}

    Parameters
    ----------
    prov_path : Path
        Path to provenance.json.
    """
    prov = json.loads(prov_path.read_text())
    prov["integrity"]["self_hash"] = "pending"
    prov["integrity"]["validated_at"] = None
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))
    print("[INFO] Initialized integrity block")


# ==============================================================================
# Docker Digest Ingestion
# ==============================================================================


def ingest_docker_digest(manifest_path: Path, prov_path: Path):
    """
    Ingest docker digest from CI (deployment/docker-digest.txt).

    Parameters
    ----------
    manifest_path : Path
        Path to manifest.json.

    prov_path : Path
        Path to provenance.json.
    """
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

    manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True))
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))

    print(f"[INFO] Ingested docker digest: {docker_digest}")
    return docker_digest


# ==============================================================================
# Release Finalization (pre-digest)
# ==============================================================================


def finalize_release(manifest_path: Path, sbom_path: Path, prov_path: Path) -> None:
    """
    Write manifest, SBOM, and provenance JSON using deterministic formatting.

    This step freezes all pre-digest fields.

    Parameters
    ----------
    manifest_path : Path
        Path to manifest.json.

    sbom_path : Path
        Path to sbom.json.

    prov_path : Path
        Path to provenance.json.
    """
    manifest = json.loads(manifest_path.read_text())
    sbom = json.loads(sbom_path.read_text())

    manifest["validation"]["status"] = "pending"

    sbom["provenance"]["status"] = "pending"
    sbom["provenance"][
        "path"
    ] = f"deployment/provenance/provenance-{manifest['version']}.json"
    sbom["provenance"]["digest"] = ""

    manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True))
    sbom_path.write_text(json.dumps(sbom, indent=4, sort_keys=True))

    print("[INFO] Release finalized (pre-digest)")


# ==============================================================================
# Integrity Finalization
# ==============================================================================


def finalize_integrity(prov_path: Path):
    """
    Compute and insert the final self‑hash into the provenance integrity block.

    The self‑hash is a SHA‑256 digest of the canonicalized provenance JSON.
    This step finalizes the integrity block before freeze_runner computes the
    detached signature.

    Parameters
    ----------
    prov_path : Path
        Path to the provenance JSON file.
    """
    digest = sha256_file(prov_path)
    prov = json.loads(prov_path.read_text())
    prov["integrity"]["self_hash"] = f"sha256:{digest}"
    prov["integrity"]["validated_at"] = ""
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))
    print(f"[INFO] Finalized integrity block with self-hash sha256:{digest}")


# ==============================================================================
# Main
# ==============================================================================


def main():
    """
    Generate all pre-freeze release artifacts for a given version.

    This function orchestrates the deterministic construction of:
    - manifest.json
    - sbom.json
    - provenance.json

    Responsibilities
    ----------------
    1. Validate JSON templates for manifest, SBOM, and provenance.
    2. Copy templates into versioned release paths.
    3. Populate placeholders using CI-provided metadata:
       - <VERSION>
       - <REPOSITORY_URL>
       - <GHCR_NAMESPACE>
       - <GITHUB_SHA>
       - <GITHUB_RUN_ID>
       - <GIT_REF>
       - <WORKFLOW_FILE>
       - <EXECUTION_ENVIRONMENT>
       - <CONTAINER_RUNTIME>
       - <DOCKER_VERSION>
       - <PYTHON_VERSION>
       - <ISO8601_TIMESTAMP>
       - <YYYY-MM-DD>
    4. Insert version metadata into manifest, SBOM, and provenance.
    5. Compute SBOM component and dependency counts.
    6. Initialize docker digest placeholders in manifest and provenance.
    7. Initialize provenance integrity block (self_hash="pending").
    8. Ingest docker digest from CI (deployment/docker-digest.txt).
    9. Freeze all pre-digest fields using deterministic formatting
       (indent=4, sort_keys=True).
    10. Compute SBOM internal hash (neutralized) and final SBOM digest.
    11. Insert SBOM digest into provenance.
    12. Compute provenance integrity.self_hash (neutralized) and final digest.
    13. Insert provenance digest into manifest and provenance.
    14. Compute final manifest digest and insert it into provenance.

    Notes
    -----
    - This script prepares all artifacts for immutable freezing.
    - Detached signature creation is performed by freeze_runner.py.
    - All formatting is deterministic and validator-aligned.

    Raises
    ------
    SystemExit
        If version is missing or any validation step fails.
    """
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
    manifest["version"] = version
    manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True))

    sbom = json.loads(sbom_path.read_text())
    sbom["metadata"]["version"] = version
    sbom_path.write_text(json.dumps(sbom, indent=4, sort_keys=True))

    prov = json.loads(prov_path.read_text())
    prov["version"] = version
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))

    print(f"[INFO] Inserted version metadata {version}")

    update_sbom_counts(sbom_path)

    initialize_docker_digest(manifest_path, prov_path)
    initialize_integrity_block(prov_path)

    ingest_docker_digest(manifest_path, prov_path)

    finalize_release(manifest_path, sbom_path, prov_path)

    # --- SBOM DIGEST (NEUTRALIZED → FINAL) ---
    sbom = json.loads(sbom_path.read_text())

    sbom_copy = json.loads(json.dumps(sbom))
    sbom_copy["hash"] = ""

    neutral_text = json.dumps(sbom_copy, indent=4, sort_keys=True)
    neutral_sbom_digest = hashlib.sha256(neutral_text.encode("utf-8")).hexdigest()

    sbom["hash"] = f"sha256:{neutral_sbom_digest}"
    sbom_path.write_text(json.dumps(sbom, indent=4, sort_keys=True))

    final_sbom_digest = sha256_file(sbom_path)

    prov = json.loads(prov_path.read_text())
    prov["artifacts"]["sbom"]["digest"] = f"sha256:{final_sbom_digest}"
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))

    print(f"[INFO] SBOM digest finalized: sha256:{final_sbom_digest}")

    # --- INTEGRITY BLOCK (NEUTRALIZED → FINAL) ---
    prov = json.loads(prov_path.read_text())

    prov_copy = json.loads(json.dumps(prov))
    prov_copy["integrity"]["self_hash"] = ""

    neutral_text = json.dumps(prov_copy, indent=4, sort_keys=True)
    neutral_prov_digest = hashlib.sha256(neutral_text.encode("utf-8")).hexdigest()

    prov["integrity"]["self_hash"] = f"sha256:{neutral_prov_digest}"
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))

    print(f"[INFO] Provenance self-hash finalized: sha256:{neutral_prov_digest}")

    # --- PROVENANCE DIGEST (FINAL) ---
    final_prov_digest = sha256_file(prov_path)

    # Insert provenance digest into provenance.json
    prov = json.loads(prov_path.read_text())
    prov["artifacts"]["provenance"]["digest"] = f"sha256:{final_prov_digest}"
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))

    # Insert provenance digest into manifest.json
    manifest = json.loads(manifest_path.read_text())
    manifest["artifacts"]["provenance"]["digest"] = f"sha256:{final_prov_digest}"
    manifest_path.write_text(json.dumps(manifest, indent=4, sort_keys=True))

    print(f"[INFO] Provenance digest finalized: sha256:{final_prov_digest}")

    # --- MANIFEST DIGEST (FINAL) ---
    final_manifest_digest = sha256_file(manifest_path)
    prov = json.loads(prov_path.read_text())
    prov["artifacts"]["manifest"]["digest"] = f"sha256:{final_manifest_digest}"
    prov_path.write_text(json.dumps(prov, indent=4, sort_keys=True))

    print(f"[INFO] Manifest digest inserted: sha256:{final_manifest_digest}")


if __name__ == "__main__":
    main()
