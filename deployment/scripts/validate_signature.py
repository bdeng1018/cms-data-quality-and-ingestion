#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path


def canonical(obj):
    return json.dumps(obj, indent=4, sort_keys=True)


def main(version):
    prov_path = Path(f"deployment/provenance/provenance-{version}.json")
    sig_path = Path(f"deployment/provenance/provenance-{version}.sig")

    if not prov_path.exists() or not sig_path.exists():
        raise FileNotFoundError("Missing provenance or signature file")

    prov = json.loads(prov_path.read_text())
    canonical_text = canonical(prov)
    expected = hashlib.sha256(canonical_text.encode()).hexdigest()
    actual = sig_path.read_text().strip()

    if expected != actual:
        raise RuntimeError("Signature mismatch")

    print("[INFO] Signature validated successfully")


if __name__ == "__main__":
    main(sys.argv[1])
