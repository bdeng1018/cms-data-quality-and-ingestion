# Frozen Versions Registry

This file records all pipeline versions that have been formally frozen.
Frozen versions are **immutable** and must never be regenerated, modified,
or overwritten. All changes must occur in future versions.

---

## v1.0.0 — Frozen on 2026-08-03

**Status:** Immutable  
**Scope:** Manifest, SBOM, provenance, signature, bundle, Docker digest  
**Rule:** No edits, no regeneration, no re-signing, no re-bundling.

Artifacts included in the freeze:

- `deployment/releases/v1.0.0.manifest.json`
- `deployment/sbom/sbom-1.0.0.json`
- `deployment/provenance/provenance-1.0.0.json`
- `deployment/provenance/provenance-1.0.0.json.sig`
- `deployment/bundles/v1.0.0.tar.gz`
- GHCR image digest for `cms-pipeline:1.0.0`

All future changes must be introduced in a new version (e.g., v1.0.1, v1.1.0).
