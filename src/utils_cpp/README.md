# utils_cpp — Deterministic C++ Mechanization Layer (Stage 01 + Stage 02)

The `utils_cpp` directory contains the deterministic C++ mechanization layer used
by the CMS Data Quality & Ingestion Pipeline. These compiled utilities provide
stable, reproducible behavior for operations where Python’s runtime variability,
dependency surface area, or performance characteristics are undesirable.

This directory implements the v1.1.0 mechanization contract and is used by:

- Stage 01 — schema validation
- Stage 02 — ingestion + row counting
- diagnostics (schema + ingestion)
- manifest + artifact registry generation
- CI/CD mechanization tests

All binaries behave deterministically across local, Docker, Compose, K8s, Helm,
and CI/CD environments.

---

## Purpose

C++ mechanization serves three goals:

### 1. **Determinism**

Compiled binaries behave identically across environments, ensuring stable results
for schema validation, row counting, and ingestion checks.

### 2. **Performance**

Large CSV operations (e.g., row counting, schema scanning) benefit from compiled
execution.

### 3. **Isolation**

C++ utilities run without Python dependencies, reducing the risk of dependency
drift or environment mismatch.

---

## Included Utilities

### `schema_validator.cpp`

Deterministic schema validator used in Stage 01.

Features:

- validates required columns
- validates column types
- produces deterministic error codes
- no reliance on Python’s type system
- stable behavior across macOS/Linux

Usage:

```bash
./schema_validator path/to/schema.json path/to/input.csv
```

Output:

```code
OK
```

or

```code
ERROR: missing column FACILITY_ID
```

---

### `csv_row_counter.cpp`

High‑performance row counter used in Stage 02 ingestion + diagnostics.

Features:

- deterministic row counting
- newline‑safe
- memory‑efficient
- stable across all environments

Usage:

```bash
./csv_row_counter path/to/file.csv
```

Output:

```code
ROWS: 152394
```

---

### `ingestion_utils.cpp`

Low‑level ingestion helpers used by Stage 02.

Features:

- deterministic file scanning
- stable newline + delimiter handling
- consistent error propagation
- used internally by Python wrappers

Usage:

```bash
./ingestion_utils path/to/file.csv
```

---

## Build Instructions

All utilities can be built using the project‑level Makefile:

```bash
make cpp-all
```

Or individually:

```bash
g++ -O2 -std=c++17 schema_validator.cpp -o schema_validator
g++ -O2 -std=c++17 csv_row_counter.cpp -o csv_row_counter
g++ -O2 -std=c++17 ingestion_utils.cpp -o ingestion_utils
```

Compiled binaries are ignored via:

```code
utils_cpp/.gitignore
```

---

## Integration with Python

Python modules call C++ utilities via `subprocess.run()`:

```python
import subprocess

result = subprocess.run(
    ["./schema_validator", schema_path, csv_path],
    capture_output=True,
    text=True
)
```

Python wrappers ensure:

- deterministic execution
- stable exit code propagation
- unified error handling
- merged diagnostics (Python + C++)
- mechanization mode recorded in manifest

---

## Mechanization Mode (Manifest + Provenance)

The pipeline records mechanization metadata:

```json
"mechanization": {
  "mode": "python+cpp",
  "schema_validator_exit_code": 0,
  "row_counter_exit_code": 0
}
```

Provenance includes:

- `mechanization_mode`
- `cpp_compiler_version`

---

## CI/CD

CI/CD validates mechanization via:

- deterministic toolchain installation
- `make cpp-all`
- `pytest -m cpp_all`
- deterministic output checks
- compiler provenance validation

Mechanization failures block the pipeline.

---

## Deployment Integration

### Dockerfile

C++ toolchain installed deterministically:

```text
g++, make, cmake, ninja-build
```

### docker-compose

Mounted read‑only:

```text
./utils_cpp:/app/utils_cpp:ro
```

### Kubernetes

Mounted read‑only:

```yml
- name: utils-cpp
  mountPath: /app/utils_cpp
  readOnly: true
```

### Helm

Mounted via values.yaml:

```yml
utils-cpp:
  hostPath: ../utils_cpp
```

---

## Error Handling

All utilities must:

- return deterministic exit codes
- write deterministic stderr
- never mutate source data
- never write outside `/app/data` or `/app/logs`
- fail fast on schema or ingestion errors

---

## Reproducibility Guarantees

C++ mechanization must produce identical output across:

- local
- Docker
- Compose
- CI/CD
- K8s
- Helm

Given identical inputs, all binaries must produce:

- identical stdout
- identical stderr
- identical exit codes

---

## Extensibility

Future deterministic utilities may include:

- fast CSV header extractors
- compiled hashing functions
- compiled artifact validators
- compiled file integrity checkers
- Stage 06 high‑performance validators

All new utilities must:

1. be deterministic
2. have a Python wrapper
3. have CI/CD tests
4. be documented in this README
5. be ignored via `.gitignore`
6. propagate exit codes deterministically

---

## Design Notes

This mechanization layer reflects the deterministic tooling used in distributed
simulation environments (e.g., JSE), where correctness, traceability, and
reproducibility are prioritized over feature complexity. Its inclusion provides a
cross‑language demonstration of integration discipline and structured pipeline
mechanization.
