#!/usr/bin/env python3
"""
freeze_runner.py

Final immutable freeze runner for the CMS Pipeline.

Purpose
-------
This script performs the *immutable freeze* step of the release pipeline.
It does **not** modify any release artifacts (manifest.json, sbom.json,
provenance.json). All digests, metadata, and integrity fields must already
be finalized by bump_version.py.

The freeze runner performs exactly three actions:

1. Load the finalized provenance JSON for the given version.
2. Canonicalize the provenance document using validator‑aligned formatting.
3. Compute a *detached signature* (SHA‑256 digest) over the canonicalized JSON.
4. Write the signature to:
       deployment/provenance/provenance-<VERSION>.sig

After writing the signature file, the freeze runner executes all validators:
- validate_manifest.py
- validate_sbom.py
- validate_provenance.py

If all validators pass, the release is considered *immutably frozen*.

Design Principles
-----------------
- Deterministic: signature is computed from canonical JSON only.
- Non‑mutating: no artifact is rewritten or altered.
- SLSA‑aligned: signature is detached and stored separately.
- Validator‑aligned: canonicalization matches the validator’s hashing logic.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    """
    Load a JSON file and return its parsed object.

    Parameters
    ----------
    path : Path
        Path to the JSON file.

    Returns
    -------
    dict
        Parsed JSON object.
    """
    return json.loads(path.read_text())


def canonicalize_for_signature(obj: dict) -> str:
    """
    Canonicalize a JSON object using the exact formatting required by
    the validators: indent=4, sort_keys=True.

    This ensures the signature is computed over the same byte sequence
    that the validators will later hash.

    Parameters
    ----------
    obj : dict
        The JSON object to canonicalize.

    Returns
    -------
    str
        Canonicalized JSON string.
    """
    return json.dumps(obj, indent=4, sort_keys=True)


def run_validator(cmd: list[str]) -> None:
    """
    Execute a validator subprocess and fail immediately if it returns
    a non-zero exit code.

    Parameters
    ----------
    cmd : list[str]
        Command list to execute, e.g. ["python", "validate_manifest.py", "1.0.0"].
    """
    print(f"[INFO] Running validator:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def freeze(version: str) -> None:
    """
    Perform the immutable freeze for a given version.

    Steps
    -----
    1. Load provenance JSON.
    2. Canonicalize provenance JSON.
    3. Compute SHA‑256 digest of canonicalized JSON.
    4. Write digest to deployment/provenance/provenance-<VERSION>.sig.
    5. Run all validators.

    Parameters
    ----------
    version : str
        Release version to freeze (e.g. "1.0.0").

    Raises
    ------
    FileNotFoundError
        If the provenance JSON file does not exist.
    """
    print(f"[INFO] Starting immutable freeze for version", version)

    # Load provenance
    prov_path = Path(f"deployment/provenance/provenance-{version}.json")
    if not prov_path.exists():
        raise FileNotFoundError(f"[ERROR] Provenance file not found: {prov_path}")

    prov = load_json(prov_path)

    # Signature output path
    sig_path = Path(f"deployment/provenance/provenance-{version}.sig")

    print("[INFO] Computing detached provenance signature...")

    # Canonicalize provenance JSON
    canonical = canonicalize_for_signature(prov)

    # Compute SHA‑256 digest of canonicalized JSON
    signature_value = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    # Write detached signature file
    sig_path.write_text(signature_value)

    print("[INFO] Running validators...")
    run_validator(["python", "deployment/scripts/validate_manifest.py", version])
    run_validator(["python", "deployment/scripts/validate_sbom.py", version])
    run_validator(["python", "deployment/scripts/validate_provenance.py", version])

    print("[INFO] Immutable freeze completed successfully — all validators passed.")


if __name__ == "__main__":
    freeze(sys.argv[1])
