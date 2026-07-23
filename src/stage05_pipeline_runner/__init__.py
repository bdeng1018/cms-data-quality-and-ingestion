"""
Stage 05 — Pipeline Orchestrator Package
================================================================================

This package contains the modules that implement Stage 05 of the CMS Data
Quality & Ingestion Pipeline.

Stage 05 is the control plane responsible for:

- Loading pipeline configuration
- Executing Stages 01 → 02 → 03 → 04 in deterministic order
- Validating Stage 04 outputs
- Generating the final pipeline summary JSON

Modules
-------
config_loader.py
    Loads and validates configs/pipeline.yml

orchestrator.py
    Executes Stages 01–04 using subprocess

run_pipeline.py
    CLI entrypoint for Stage 05; builds summary JSON

This package is intentionally minimal and does not produce logs.
"""
