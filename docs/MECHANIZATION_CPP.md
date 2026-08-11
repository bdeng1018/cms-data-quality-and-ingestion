# Mechanization Layer (C++ Deterministic Execution) — v1.1.0

The CMS Data Quality & Ingestion Pipeline includes a deterministic C++ mechanization
layer used for high‑performance, reproducible validation and ingestion operations.
Mechanization is introduced in **v1.1.0** and applies to:

- Stage 01 — schema validation
- Stage 02 — raw ingestion + row counting
- Diagnostics (Stage 01 + Stage 02)
- CI/CD mechanization tests
- Docker / Compose / K8s / Helm deployments

Mechanization ensures that critical operations behave identically across all
environments, independent of Python’s runtime variability.

---

## Goals

### 1. Determinism

Compiled C++ binaries produce identical output across:

- macOS
- Linux
- Docker
- docker‑compose
- Kubernetes
- Helm
- CI/CD

### 2. Performance

Large CSV operations (schema scanning, row counting) benefit from compiled execution.

### 3. Isolation

C++ utilities run without Python dependencies, reducing risk of:

- dependency drift
- interpreter differences
- nondeterministic behavior

---

## Components

### `schema_validator.cpp` (Stage 01)

Validates:

- required columns
- column presence
- structural correctness

Outputs deterministic:

- stdout
- stderr
- exit codes

### `csv_row_counter.cpp` (Stage 02)

Counts rows deterministically:

- newline‑safe
- memory‑efficient
- stable across platforms

### `ingestion_utils.cpp`

Low‑level ingestion helpers used internally by wrappers.

---

## Directory Layout

```text
src/utils_cpp/
├── csv_row_counter.cpp
├── csv_row_counter
├── ingestion_utils.cpp
├── schema_validator.cpp
├── run_csv_row_counter.py
└── .gitignore
```

---

## Build Instructions

### Project‑level build (recommended)

```bash
make cpp-all
```

### Individual builds

```bash
g++ -O2 -std=c++17 schema_validator.cpp -o schema_validator
g++ -O2 -std=c++17 csv_row_counter.cpp -o csv_row_counter
g++ -O2 -std=c++17 ingestion_utils.cpp -o ingestion_utils
```

All compiled binaries are ignored via:

```code
utils_cpp/.gitignore
```

---

## Python Integration

Python wrappers call C++ binaries via deterministic subprocess execution:

```python
import subprocess

result = subprocess.run(
    ["./csv_row_counter", csv_path],
    capture_output=True,
    text=True
)
```

Wrappers ensure:

- deterministic exit code propagation
- unified error handling
- merged diagnostics (Python + C++)
- manifest mechanization fields are populated

---

## Manifest Integration

Mechanization metadata appears in:

```code
deployment/releases/<version>.manifest.json
```

Example:

```json
"mechanization": {
  "mode": "python+cpp",
  "schema_validator_exit_code": 0,
  "row_counter_exit_code": 0,
  "cpp_compiler_version": "g++-13"
}
```

---

## Provenance Integration

Provenance includes:

- `mechanization_mode`
- `cpp_compiler_version`
- deterministic mechanization logs

---

## Logging Integration

Mechanization logs are written to:

```code
logs/mechanization.log
```

Fluent Bit ingests them via:

```code
[INPUT]
    Name tail
    Path /app/logs/mechanization.log
```

---

## Deployment Integration

### Dockerfile

Installs deterministic C++ toolchain:

```text
g++, make, cmake, ninja-build
```

### docker-compose

Mounts mechanization layer read‑only:

```code
./utils_cpp:/app/utils_cpp:ro
```

### Kubernetes

Mounts mechanization layer read‑only:

```yml
- name: utils-cpp
  mountPath: /app/utils_cpp
  readOnly: true
```

### Helm

Values include:

```yml
utils-cpp:
  hostPath: ../utils_cpp
```

---

## CI/CD Integration

CI/CD pipeline:

- installs deterministic C++ toolchain
- builds mechanization layer (`make cpp-all`)
- runs mechanization tests (`pytest -m cpp_all`)
- validates deterministic output
- records mechanization exit codes

Mechanization failures block the pipeline.

---

## Testing

Mechanization tests live under:

```code
tests/utils_cpp/
```

Tests verify:

- deterministic output
- correct exit codes
- Python wrapper behavior
- ingestion integration

---

## Future Extensions

Planned additions:

- Stage 06 compiled validators
- compiled hashing functions
- compiled artifact integrity checkers
- compiled CSV header extractors
- mechanization performance metrics

All new utilities must:

1. be deterministic
2. have Python wrappers
3. have CI/CD tests
4. be documented here
5. propagate exit codes deterministically

---

## Design Notes

The mechanization layer reflects deterministic tooling used in distributed
simulation environments (e.g., JSE), prioritizing:

- correctness
- reproducibility
- traceability
- isolation

Its inclusion demonstrates cross‑language integration discipline and structured
pipeline mechanization.
