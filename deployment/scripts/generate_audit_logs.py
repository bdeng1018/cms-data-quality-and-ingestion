#!/usr/bin/env python3
"""
generate_audit_logs.py

Generates a deterministic audit log using:
- manifest.provenance
- SBOM metadata
- timestamp
- execution context
- integrity hashes (SHA-256)

Output is a single log file (text) with structured sections suitable for
governance, compliance, CI/CD pipelines, and audit trails.
"""

import argparse
import datetime
import hashlib
import json
import os
import socket
import sys
from pathlib import Path


def load_json(path: Path):
    """Load JSON file with deterministic error handling."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load JSON '{path}': {e}")
        sys.exit(1)


def sha256_file(path: Path):
    """Compute SHA-256 hash of a file."""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    except Exception as e:
        print(f"[ERROR] Failed to hash file '{path}': {e}")
        sys.exit(1)


def write_section(f, title):
    """Write a formatted section header."""
    f.write(f"\n=== {title} ===\n")


def main():
    parser = argparse.ArgumentParser(description="Generate audit logs")
    parser.add_argument("--manifest", required=True, help="Path to manifest.provenance")
    parser.add_argument("--sbom", required=True, help="Path to SBOM JSON")
    parser.add_argument("--out", required=True, help="Output audit log file")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    sbom_path = Path(args.sbom)
    out_path = Path(args.out)

    if not manifest_path.exists():
        print(f"[ERROR] Manifest file not found: {manifest_path}")
        sys.exit(1)

    if not sbom_path.exists():
        print(f"[ERROR] SBOM file not found: {sbom_path}")
        sys.exit(1)

    print("[INFO] Loading manifest and SBOM...")
    manifest = load_json(manifest_path)
    sbom = load_json(sbom_path)

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    hostname = socket.gethostname()
    user = os.getenv("USER", "unknown")
    cwd = Path.cwd()

    manifest_hash = sha256_file(manifest_path)
    sbom_hash = sha256_file(sbom_path)

    print("[INFO] Writing audit log...")

    with open(out_path, "w") as f:
        write_section(f, "Audit Metadata")
        f.write(f"timestamp: {timestamp}\n")
        f.write(f"host: {hostname}\n")
        f.write(f"user: {user}\n")
        f.write(f"cwd: {cwd}\n")
        f.write("executor: python\n")

        write_section(f, "Integrity")
        f.write(f"manifest_sha256: {manifest_hash}\n")
        f.write(f"sbom_sha256: {sbom_hash}\n")

        write_section(f, "Provenance")
        for key, value in manifest.items():
            f.write(f"{key}: {value}\n")

        write_section(f, "SBOM Summary")
        f.write(f"sbom_version: {sbom.get('sbom_version', '')}\n")
        f.write(f"pipeline_version: {sbom.get('pipeline_version', '')}\n")
        f.write(f"deployment_version: {sbom.get('deployment_version', '')}\n")
        f.write(f"components_count: {len(sbom.get('components', []))}\n")

        write_section(f, "Components")
        for idx, comp in enumerate(sbom.get("components", [])):
            name = comp.get("name", "")
            version = comp.get("version", "")
            source = comp.get("source", "")
            f.write(f"{idx+1}. {name} — {version} — {source}\n")

        write_section(f, "Status")
        f.write("audit_status: success\n")

    print(f"[OK] Audit log written to {out_path}")


if __name__ == "__main__":
    main()
