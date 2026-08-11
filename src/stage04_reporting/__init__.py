"""
Stage 04 — Reporting Package
================================================================================

This package implements Stage 04 of the CMS Data Quality & Ingestion Pipeline:
the deterministic reporting layer responsible for transforming Stage 03 quality
artifacts into human‑interpretable, facility‑level and dataset‑level outputs.

Stage 04 responsibilities include:

- Generating facility‑level health reports
- Producing dataset‑level summaries
- Formatting column‑level and metric‑level outputs
- Writing deterministic JSON/CSV artifacts to `data/stage04_processed/`
- Preparing the reporting index consumed by Stage 05

Modules
-------
report_engine.py
    Core reporting logic; transforms Stage 03 metrics into structured outputs.

report_formatter.py
    Applies deterministic formatting rules for JSON/CSV report artifacts.

report_writer.py
    Writes all Stage 04 artifacts to the canonical processed directory.

run_reporting.py
    CLI entrypoint for Stage 04; executes the reporting workflow end‑to‑end.

Notes
-----
This package contains no side effects beyond writing deterministic artifacts.
It performs no ingestion, cleaning, or quality checks.

Stage 04 outputs are validated by Stage 05 and included in the final pipeline
summary. Branch 1 contains no PHI/PII; all reporting is deterministic and
reproducible across environments.
"""
