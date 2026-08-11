"""
Stage 03 — Data Quality Engine
================================================================================

This package implements Stage 03 of the CMS Data Quality & Ingestion Pipeline:
the deterministic quality‑checking layer responsible for evaluating raw POS/QIES
ingestion outputs (Stage 02) and producing intermediate quality artifacts used by
Stage 04 reporting and Stage 05 orchestration.

Stage 03 responsibilities include:

- Running baseline quality checks on POS/QIES data
- Computing facility‑level and column‑level metrics
- Generating deterministic intermediate artifacts:
    - `facility_metrics.csv`
    - `column_profiles.json`
    - `quality_summary.json`
- Providing structured quality metadata for downstream reporting
- Ensuring all outputs are reproducible across environments

Modules
-------
quality_checks.py
    Implements individual quality checks and validation rules.

quality_engine.py
    Coordinates quality checks, aggregates results, and produces artifacts.

quality_writer.py
    Writes deterministic Stage 03 outputs to `data/stage03_intermediate/`.

run_quality.py
    CLI entrypoint for Stage 03; executes the full quality workflow.

Exports
-------
QualityReport
run_quality_checks

Notes
-----
Stage 03 performs no ingestion, cleaning, or reporting. It evaluates structure,
consistency, and completeness of Stage 02 outputs and prepares artifacts consumed
by Stage 04 and validated by Stage 05.

Branch 1 contains no PHI/PII; all quality checks are deterministic.
"""

from .quality_checks import QualityReport, run_quality_checks

__all__ = ["run_quality_checks", "QualityReport"]
