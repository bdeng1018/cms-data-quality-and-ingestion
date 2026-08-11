"""
Stage 01 — Canonical Schema Definition & Deterministic Validation
================================================================================

This package implements Stage 01 of the CMS Data Quality & Ingestion Pipeline:
the canonical schema layer responsible for loading the official CMS schema,
performing deterministic structural validation, and integrating with the v1.1.0
C++ mechanization validator.

Stage 01 responsibilities include:

- Loading the canonical JSON schema from `data/stage01_schema/schema.json`
- Performing structural and type validation on raw POS/QIES inputs
- Running the deterministic C++ schema validator (v1.1.0)
- Propagating mechanization exit codes to downstream stages
- Emitting schema‑level diagnostics for ingestion and quality checks
- Providing the foundational schema contract for Stages 02–05

Modules
-------
schema_loader.py
    Loads and parses the canonical JSON schema.

schema_validator.py
    Performs Python‑based structural and type validation.

cpp_schema_validator.cpp
    Deterministic C++ schema validator used for mechanization (v1.1.0).

run_cpp_schema_validator.py
    Python wrapper for invoking the C++ validator via deterministic subprocess.

Notes
-----
Stage 01 defines the authoritative schema for the entire pipeline. All downstream
stages (ingestion, quality, reporting, orchestration) rely on this schema for
column presence, type expectations, and structural guarantees.

Branch 1 contains no PHI/PII; all schema validation is deterministic and
reproducible across local, Docker, Compose, Kubernetes, Helm, and CI/CD.
"""
