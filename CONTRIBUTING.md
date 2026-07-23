# CONTRIBUTING.md

Thank you for your interest in contributing to **cms-data-quality-and-ingestion**.
This project implements a reproducible, multi‑stage CMS ingestion and data‑quality pipeline.
Branch 1 covers Stages 01–05 (schema → ingestion → quality → reporting → pipeline runner).

This document describes how to contribute code, documentation, tests, and diagnostics.

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

Each stage has:

- a dedicated README
- diagnostics scripts
- tests
- logging
- Makefile targets

Data artifacts are stored under:

```text
data/stageXX_*
```

Logs are stored under:

```text
logs/
```

---

## 🧰 Development Environment

Create the environment:

```bash
make env
conda activate pos_qies_pipeline
```

This project uses a single `environment.yml` file for both runtime and development dependencies.
Contributors should ensure the following tools are installed inside the environment:

- pytest
- black
- isort
- flake8
- mypy (optional)

If any of these are missing, install them manually:

```bash
pip install pytest black isort flake8 mypy
```

These tools ensure consistent formatting, linting, and testing across all pipeline stages.

---

## Diagram Workflow

All diagrams are maintained in Mermaid (.md) and exported to PNG.

Both files are committed to the repo:

- `diagrams/*.md`  → source of truth
- `diagrams/*.png` → rendered artifact

Use VS Code Mermaid preview or Mermaid CLI for PNG export.
Do not commit SVG or draw.io files unless explicitly needed.

---

## 🛠 Running the Pipeline

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
    --file data/stage02_raw/pos_q2_2026.csv \
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

Tests should follow these guidelines:

- use `tmp_path` for filesystem isolation
- avoid writing to real pipeline directories
- prefer synthetic POS/QIES fixtures
- ensure deterministic outputs
- test both engine logic and writer behavior

---

## 🧼 Code Style

This project follows:

- **Black** for formatting
- **isort** for import ordering
- **flake8** for linting
- **mypy** for optional type checking

Recommended workflow:

```bash
black src tests
isort src tests
flake8 src tests
```

---

## 📘 Documentation

Each stage must include:

- a `README.md` describing inputs, outputs, architecture, and runner behavior
- module‑level docstrings
- function‑level docstrings using NumPy‑style format

Example docstring:

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

Contributors should:

- use `logging.getLogger(__name__)`
- avoid printing to stdout
- ensure logs are meaningful and structured

---

## 🧱 Adding a New Stage

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

Branch 1 is **fully deterministic** (Stages 01–06 infrastructure only).
AI/RAG/agentic inference will be introduced in **Branch 2** and should not be added to Branch 1.

---

## 🔄 Makefile Workflow

The Makefile defines:

- stage execution
- diagnostics
- environment creation
- testing
- reset/cleanup

Contributors should annotate new targets using:

```code
target: ## Description
```

This enables `make help`.

---

## 🧭 Branching & Versioning

This project uses semantic versioning:

- `0.1.x` — Branch 1 (Stages 01–05)
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
- avoid large, multi‑stage changes in a single PR

---

## 🛡 Code of Conduct

See `CODE_OF_CONDUCT.md` for community guidelines.

---

## 📬 Contact

Maintainer: **Brian Deng**  <br>
Location: Los Angeles, CA <br>
Email: **<bdeng.data.pipelines@gmail.com>** <br>
Focus: healthcare data engineering, analytics systems design, scientific computing, data quality & governance, technical writing
