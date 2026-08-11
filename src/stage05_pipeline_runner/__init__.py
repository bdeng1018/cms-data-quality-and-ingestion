"""
Stage 05 — Pipeline Orchestrator Package
================================================================================

This package implements Stage 05 of the CMS Data Quality & Ingestion Pipeline:
the deterministic control plane responsible for executing Stages 01–04,
collecting mechanization metadata, validating reporting outputs, and generating
the final pipeline summary artifact.

Stage 05 responsibilities include:

- Loading and validating `configs/pipeline.yml`
- Executing Stages 01 → 02 → 03 → 04 in deterministic order
- Enforcing deterministic subprocess execution for mechanization (v1.1.0)
- Collecting mechanization exit codes and compiler provenance
- Validating Stage 04 reporting artifacts for completeness and consistency
- Generating the final `pipeline_summary.json` with timestamps, duration,
  per‑stage status, warnings, and mechanization metadata

Modules
-------
config_loader.py
    Loads and validates pipeline configuration.

orchestrator.py
    Executes Stages 01–04, merges mechanization metadata, and enforces
    deterministic subprocess behavior.

run_pipeline.py
    CLI entrypoint for Stage 05; produces the final pipeline summary JSON.

Notes
-----
Stage 05 is intentionally minimal: it does not modify data, perform cleaning,
or generate metrics. It orchestrates, validates, and summarizes.

Branch 1 is fully deterministic and contains no PHI/PII. Stage 06+ will build
on Stage 05 outputs to introduce AI/RAG/LLM-driven augmentation.
"""
