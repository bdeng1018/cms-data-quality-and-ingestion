# Documentation Index — CMS Data Quality & Ingestion Pipeline

This index provides a structured overview of all documentation for the CMS Data Quality & Ingestion Pipeline.  
Use this as the entry point to navigate architecture, onboarding, data contracts, and stage‑specific design docs.

---

## 1. High‑Level Documentation

### [README.md](../README.md)

Project overview, goals, quickstart, and repository structure.

### [ONBOARDING.md](ONBOARDING.md)

Developer setup, environment configuration, Makefile workflow, and local development instructions.

### [ARCHITECTURE.md](ARCHITECTURE.md)

High‑level system design, stage responsibilities, directory layout, logging, configuration, and testing architecture.

### [PIPELINE_FLOW.md](PIPELINE_FLOW.md)

End‑to‑end data flow, artifact flow, stage transitions, and diagnostics execution.

---

## 2. Data Contract Documentation

### [DATA_DICTIONARY.md](DATA_DICTIONARY.md)

Definitions for all fields in `cleaned_data.csv` (Stage 02 output).  
Includes types, descriptions, and semantic meaning.

### [SCHEMA_REFERENCE.md](SCHEMA_REFERENCE.md)

Reference for `schema.json` (Stage 01 output).  
Documents field types, required fields, and schema evolution rules.

---

## 3. Stage‑Specific Design Documentation

### [STAGE05_DESIGN.md](STAGE05_DESIGN.md)

Deep dive into the Stage 05 orchestrator:  
execution order, configuration loading, error handling, summary generation, and cross‑stage coordination.

---

## 4. Additional Project Documentation

### [CONTRIBUTING.md](../CONTRIBUTING.md)

Contribution guidelines, PR workflow, coding standards, and branching strategy.

### [CHANGELOG.md](../CHANGELOG.md)

Version history and release notes.

### [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)

Community and contributor behavior guidelines.

### [SECURITY.md](../SECURITY.md)

Security reporting process and vulnerability disclosure guidelines.

---

## 5. Visual Diagrams

### `diagrams/pipeline_architecture.png`

High‑level pipeline architecture diagram.

### `diagrams/schema_overview.png`

Schema visualization for Stage 01 and Stage 02 outputs.

---

## 6. Where to Go Next

If you're evaluating the pipeline:

- Start with **README.md**  
- Then read **ARCHITECTURE.md**  
- Follow with **PIPELINE_FLOW.md**  
- Review **DATA_DICTIONARY.md** and **SCHEMA_REFERENCE.md**  
- Finish with **STAGE05_DESIGN.md**

If you're onboarding as a developer:

- Start with **ONBOARDING.md**  
- Then explore the `src/` stage folders  
- Use diagnostics under `scripts/diagnostics/`  
- Run tests under `tests/`

---

## 7. Maintainer

Maintainer: Brian Deng <br>
Email: <bdeng.data.pipelines@gmail.com> <br>
GitHub: <https://github.com/bdeng1018>
