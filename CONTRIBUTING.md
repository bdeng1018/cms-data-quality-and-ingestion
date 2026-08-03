# CONTRIBUTING.md

Thank you for your interest in contributing to **cms-data-quality-and-ingestion**.  
This project implements a reproducible, multi‑stage CMS ingestion and data‑quality pipeline.  
Branch 1 covers Stages 01–05 (schema → ingestion → quality → reporting → pipeline runner) and is fully deterministic.

This document describes how to contribute code, documentation, tests, diagnostics, and deployment‑related changes.

---

## 📦 Repository Structure

The project is organized into five pipeline stages:

```text
src/
  stage01_schema_definition/
  stage02_raw_ingestion/
  stage03_data_quality/
  stage04_reporting/
  stage05_pipeline_runner/
```

Each stage includes:

- a dedicated README  
- diagnostics scripts  
- tests  
- logging  
- Makefile targets  

Data artifacts live under:

```text
data/stageXX_*/
```

Logs live under:

```text
logs/
```

Deployment artifacts live under:

```text
deployment/
```

Deployment includes:

- `deployment/Dockerfile`
- `deployment/Makefile.deploy`
- root‑level `compose.yml`
- governance, compliance, SBOM, provenance, versioning contracts
- Helm, Terraform, logging, monitoring, security subsystems

---

## 🧰 Development Environment

Create and activate the environment:

```bash
make env
conda activate pos_qies_pipeline
```

This project uses a single `environment.yml` for runtime + development dependencies.

Inside the environment, contributors should ensure the following tools are available:

- pytest  
- black  
- isort  
- ruff  
- flake8  
- mypy (optional)

If any are missing:

```bash
pip install pytest black isort ruff flake8 mypy
```

These tools ensure consistent formatting, linting, and testing across all pipeline stages.

---

## 🗺 Diagram Workflow

All diagrams are maintained in Mermaid (`.md`) and exported to PNG.

Both files are committed:

- `diagrams/*.md` → source of truth  
- `diagrams/*.png` → rendered artifact  

Use VS Code Mermaid preview or Mermaid CLI for PNG export.  
Do not commit SVG or draw.io files unless explicitly required.

---

## 🛠 Running the Pipeline (Local)

Each stage can be executed individually via Makefile:

```bash
make stage01
make stage02
make stage03
make stage04
make stage05
```

Diagnostics scripts live under:

```text
scripts/diagnostics/stageXX/
```

Example:

```bash
python scripts/diagnostics/stage03/check_quality.py \
    --file data/stage02_cleaned/cleaned_data.csv \
    --type pos
```

---

## 🧪 Testing

All tests are located under:

```text
tests/stageXX_*/
```

Run the full suite:

```bash
make test
```

Or run a specific stage:

```bash
pytest tests/stage03_data_quality
```

Testing guidelines:

- use `tmp_path` for filesystem isolation  
- avoid writing to real pipeline directories  
- prefer synthetic POS/QIES fixtures  
- ensure deterministic outputs  
- test both engine logic and writer behavior  
- ensure diagnostics scripts behave consistently  

---

## 🧼 Code Style

This project follows:

- **Black** for formatting  
- **isort** for import ordering  
- **ruff** and **flake8** for linting  
- **mypy** for optional type checking  

Recommended workflow:

```bash
black src tests
isort src tests
ruff check src tests
flake8 src tests
```

---

## 📘 Documentation

Each stage must include:

- a `README.md` describing inputs, outputs, architecture, and runner behavior  
- module‑level docstrings  
- function‑level docstrings using NumPy‑style format  

Example:

```python
def compute_metrics(df: pd.DataFrame) -> dict:
    """
    Compute dataset-level quality metrics.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.

    Returns
    -------
    dict
        Dictionary containing row counts, null counts, and drift indicators.
    """
```

---

## 📑 Logging

All stages use YAML‑configured logging under:

```text
configs/logging.yml
```

Log files are written to:

```text
logs/ingestion.log
logs/quality.log
logs/runner.log
```

Contributor guidelines:

- use `logging.getLogger(__name__)`  
- avoid printing to stdout  
- ensure logs are structured and meaningful  

---

## 🧱 Adding or Modifying a Stage

To add or modify a pipeline stage:

1. Create a new directory under `src/`  
2. Add a `README.md`  
3. Add `__init__.py`  
4. Add engine, formatter, writer, and runner modules (if applicable)  
5. Add diagnostics scripts under `scripts/diagnostics/stageXX/`  
6. Add tests under `tests/stageXX_*/`  
7. Update the Makefile  
8. Update the root README  
9. Update `CHANGELOG.md` under `[Unreleased]`  

### Branch 1 Note

Branch 1 is **fully deterministic** (Stages 01–05 + Stage 06 infrastructure only).  
AI/RAG/agentic inference arrives in **Branch 2** and should not be added to Branch 1.

---

## 🔄 Makefile Workflow

The Makefile defines:

- stage execution  
- diagnostics  
- environment creation  
- testing  
- reset/cleanup  
- deployment validation (provenance, SBOM, drift, audit)  

Annotate new targets using:

```makefile
target: ## Description
```

This enables `make help`.

---

## 🏗 Deployment Contributions

Deployment contributions must respect deterministic contracts:

- `deployment/Dockerfile`
- root‑level `compose.yml`
- `deployment/Makefile.deploy`
- provenance rules
- SBOM rules
- versioning rules
- governance rules
- compliance rules
- access control rules

Deployment changes **must not** break determinism.

All deployment changes require:

- SBOM update
- RELEASE_NOTES update
- provenance update
- CI/CD validation

---

## 🧭 Branching & Versioning

This project uses semantic versioning:

- `0.1.x` — Branch 1 (Stages 01–05)  
- `0.2.x` — Transformation + enrichment  
- `0.3.x` — Dashboard + reporting layer  

All changes must be recorded in `CHANGELOG.md` under:

```text
## [Unreleased]
```

Tags are created only when a milestone is complete.

---

## 🤝 Pull Requests

Pull requests should:

- be atomic  
- include tests  
- update documentation  
- update `CHANGELOG.md`  
- pass linting and formatting  
- avoid multi‑stage changes in a single PR  
- avoid modifying deployment contracts without justification  
- preserve deterministic behavior  

---

## 🛡 Code of Conduct

See `CODE_OF_CONDUCT.md` for community guidelines.

---

## 📬 Contact

Maintainer: **Brian Deng**  
Location: Los Angeles, CA  
Email: **<bdeng.data.pipelines@gmail.com>**  

Focus: healthcare data engineering, analytics systems design, scientific computing, data quality & governance, technical writing
