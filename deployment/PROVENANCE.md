# PROVENANCE.md

CMS Data Quality & Ingestion Pipeline — Provenance Contract (v1.1.1)

## 1. Purpose

This document defines the deterministic provenance model for the CMS Data Quality & Ingestion Pipeline.
Provenance ensures every pipeline run is reproducible, auditable, environment‑stable, and mechanization‑verified.

Provenance metadata appears in:

- `manifest.json`
- `pipeline_summary.json`
- SBOM
- CI/CD logs
- deployment annotations

---

## 2. Deterministic Provenance Fields

Each pipeline run must include the following provenance fields:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
mechanization_version
sbom_version
executor
hostname
python_version
os_version
docker_image (optional)
mechanization_mode
cpp_compiler_version (optional)
```

All fields must be present in local, Docker, Compose, and CI/CD environments.

---

## 3. Execution Provenance

Execution provenance records the runtime environment:

```yaml
executor: "local | docker | compose | ci"
hostname: "string"
python_version: "3.x.x"
os_version: "Ubuntu 22.04 | macOS | Windows"
docker_image: "optional"
```

Rules:

- `executor` must match the actual runtime
- `hostname` must be captured deterministically
- `python_version` must match the active interpreter
- `os_version` must reflect the real environment

---

## 4. Mechanization Provenance

Mechanization provenance records deterministic C++ execution:

```yaml
mechanization_mode: "python-only | python+cpp"
schema_validator_exit_code: 0
row_counter_exit_code: 0
cpp_compiler_version: "g++ 13.x.x"
```

Rules:

- mechanization mode must reflect actual execution
- exit codes must be recorded for both C++ tools
- compiler version must be included for Docker + CI/CD

Mechanization provenance is required for reproducibility.

---

## 5. Version Provenance

Version provenance ensures all version layers propagate correctly:

```yaml
pipeline_version: "1.1.1"
schema_version: "1.1.1"
artifact_version: "1.1.1"
manifest_version: "1.1.1"
deployment_version: "1.1.1"
mechanization_version: "1.1.1"
sbom_version: "1.1.1"
```

Rules:

- all version fields must be present
- version propagation must be deterministic
- mismatches cause pipeline failure

---

## 6. Artifact Provenance

Artifact provenance records:

```yaml
artifact_registry_path: "data/stage05_reports/artifact_registry.json"
artifact_registry_hash: "sha256"
artifact_list:
  - dataset_summary.json
  - top_facilities.csv
  - bottom_facilities.csv
  - sparse_columns.json
  - column_health.json
  - pipeline_summary.json
```

Rules:

- artifact list must be deterministic
- artifact hashes must be stable
- registry path must be canonical

---

## 7. Deployment Provenance

Deployment provenance records:

```yaml
dockerfile: "deployment/Dockerfile"
compose: "compose.yml"
helm_chart: "deployment/helm/Chart.yml"
terraform: "deployment/terraform/main.tf"
deployment_version: "1.1.1"
```

Rules:

- deployment_version must match CI/CD logs
- deployment artifacts must be immutable
- deployment provenance must be included in SBOM

---

## 8. CI/CD Provenance

CI/CD provenance records:

```yaml
workflow: "ci.yml"
runner: "github-actions"
cache_state: "hit | miss"
```

Rules:

- CI/CD provenance must be included in release bundles
- workflow name must be deterministic
- cache state must be logged

---

## 9. Provenance Validation

Provenance must be validated by:

- Stage 05 diagnostics
- manifest schema validation
- SBOM validation
- CI/CD provenance checks

Validation rules:

- all required fields must be present
- all version fields must match
- mechanization exit codes must be valid
- timestamps must be consistent
- hashes must match source files

---

## 10. Future Extensions

Future provenance fields may include:

- distributed execution provenance
- multi‑region deployment provenance
- RAG/AI retrieval provenance
- inference trace provenance
- OpenTelemetry provenance
