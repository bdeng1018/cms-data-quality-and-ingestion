# Style Guide

A unified coding, documentation, and workflow standard for the **cms-data-quality-and-ingestion** deterministic pipeline. This guide ensures consistency across contributors, stages, diagnostics, and deployment artifacts.

---

## 1. Python Code Style

### 1.1 Formatting

- Use **Black** for all formatting.
- Use **isort** with `--profile black`.
- No manual formatting overrides unless absolutely necessary.

### 1.2 Imports

- Standard library → third‑party → local modules.
- Avoid wildcard imports.
- Use absolute imports for all pipeline modules.

Example:

```python
import json
from pathlib import Path

import pandas as pd

from stage03_data_quality.metrics import compute_metrics
```

### 1.3 Type Hints

- Required for all functions.
- Use `typing` or `collections.abc` for generics.
- Avoid `Any` unless unavoidable.

Example:

```python
def load_csv(path: Path) -> pd.DataFrame:
    ...
```

### 1.4 Function Design

- Pure functions preferred.
- No hidden side effects.
- Deterministic behavior only.

### 1.5 Logging

- Use `logging` module.
- No `print()` in production code.
- Use structured logging where possible.

---

## 2. Directory & File Structure

### 2.1 Stage Layout

Each stage must contain:

- `run_*.py`
- `README.md`
- `utils/` (optional)
- `tests/` (optional)

Example:

```code
src/stage03_data_quality/
    run_quality.py
    README.md
    metrics.py
    validators.py
```

### 2.2 Data Layout

All pipeline outputs follow deterministic paths:

```code
data/stage01_schema/
data/stage02_raw/
data/stage03_intermediate/
data/stage04_processed/
data/stage05_reports/
```

No other directories may store pipeline outputs.

---

## 3. Makefile Standards

### 3.1 Target Naming

- Use lowercase.
- Use hyphens only when necessary.
- Stage targets must follow:

```code
stage01
stage02
stage03
stage04
stage05
```

### 3.2 Required Targets

- `env`
- `reset`
- `diagnostics`
- `lint`
- `test`
- `run`

### 3.3 Deterministic Execution

Makefile targets must:

- avoid randomness
- avoid non‑reproducible timestamps
- avoid external network calls unless in deployment layer

---

## 4. Documentation Standards

### 4.1 Markdown Rules

- Use H1 only for document title.
- Use H2/H3 for structure.
- No trailing whitespace.
- Code blocks must specify language.

### 4.2 Diagrams

All diagrams must live in:

```code
diagrams/
```

### 4.3 Stage Documentation

Each stage must include:

- purpose
- inputs
- outputs
- invariants
- deterministic guarantees

---

## 5. Testing Standards

### 5.1 Pytest Structure

Tests must live under:

```code
tests/
```

### 5.2 Test Types

- unit tests → required
- integration tests → optional
- regression tests → optional

### 5.3 Assertions

Use explicit assertions:

```python
assert df.shape[0] > 0
```

Avoid implicit truthiness.

---

## 6. Deterministic Pipeline Rules

### 6.1 No Randomness

Randomness is prohibited unless:

- seeded explicitly
- documented
- deterministic across runs

### 6.2 No External Calls

Stages may not:

- call APIs
- fetch remote data
- depend on external state

### 6.3 Reproducibility

Given identical inputs:

- outputs must match bit‑for‑bit
- logs must match except timestamps
- manifests must match except timestamps

---

## 7. Deployment Style Rules

### 7.1 YAML

- 2‑space indentation
- lowercase keys
- no trailing comments

### 7.2 Docker

- one process per container
- pinned versions only
- no `latest` tags

### 7.3 Terraform

- variables must be typed
- outputs must be documented
- modules must be isolated

---

## 8. Git & Branching

### 8.1 Branch Names

Use:

```code
feature/<name>
fix/<name>
stageXX/<name>
```

### 8.2 Commit Messages

Format:

```code
<type>: <short description>

Long description (optional)
```

Types:

- `feat`
- `fix`
- `docs`
- `refactor`
- `infra`
- `test`

### 8.3 Pull Requests

Must include:

- summary
- screenshots (if applicable)
- test results
- deterministic guarantees

---

## 9. Linting & Diagnostics

### 9.1 Linting

Run:

```bash
make lint
```

Includes:

- black
- isort
- pylint

### 9.2 Diagnostics

Run:

```bash
make diagnostics
```

Includes:

- schema checks
- quality checks
- reporting checks

---

## 10. Glossary Reference

All terminology must align with:

```code
docs/GLOSSARY.md
```
