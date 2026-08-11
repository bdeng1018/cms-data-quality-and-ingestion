"""
CMS Data Quality & Ingestion Pipeline (Branch 1 — Deterministic Execution)

This package contains the complete Branch 1 deterministic pipeline:

- Stage 01: Canonical schema definition and validation
    - Python validator
    - Deterministic C++ schema validator (v1.1.0)
    - Schema loader + manifest integration

- Stage 02: POS/QIES raw ingestion and minimal structural checks
    - CSV/Parquet loaders
    - Deterministic C++ row counter (v1.1.0)
    - Ingestion metadata + mechanization exit codes

- Stage 03: Data quality engine and intermediate metrics
    - Column profiles
    - Facility-level metrics
    - Quality summary artifacts

- Stage 04: Reporting engine and facility-level outputs
    - Report formatter
    - Dataset summaries
    - Facility health reports

- Stage 05: Pipeline orchestrator and summary generator
    - Deterministic stage sequencing
    - Mechanization metadata collection
    - Final pipeline summary artifact

Branch 1 is fully deterministic and contains no PHI/PII.
All execution is reproducible across local, Docker, Compose, Kubernetes, Helm, and CI/CD.

Future development (Stage 06+) will introduce AI/RAG/LLM-driven insights and
agentic quality analysis built on top of Stage 05 outputs.
"""
