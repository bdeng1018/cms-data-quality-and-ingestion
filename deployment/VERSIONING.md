# CMS Data Quality & Ingestion Pipeline — Versioning Contract

## Documentation Contract

This document defines the deterministic versioning rules for the CMS Data Quality & Ingestion Pipeline.
Versioning applies to pipeline releases, schemas, artifacts, manifests, deployment configurations, mechanization metadata, and provenance.

### Determinism Guarantees

- pinned semantic versioning rules
- pinned schema versioning
- pinned artifact versioning
- pinned manifest versioning
- pinned deployment versioning
- pinned mechanization versioning
- reproducible version propagation

### Side Effects

- enforces reproducible pipeline behavior
- enforces deterministic artifact generation
- enforces stable schema evolution
- enforces consistent deployment upgrades
- enforces deterministic mechanization behavior

---

## 1. Semantic Versioning (Pipeline)

The pipeline uses **Semantic Versioning (SemVer)**:

```text
MAJOR.MINOR.PATCH
```

### MAJOR

Increment when:

- schema changes break compatibility
- artifact formats change
- manifest structure changes
- pipeline execution semantics change
- mechanization behavior changes (e.g., new C++ validators)

### MINOR

Increment when:

- new features are added
- new metrics or diagnostics are added
- new artifacts are added
- new deployment options are added
- new mechanization utilities are added

### PATCH

Increment when:

- bugs are fixed
- diagnostics are corrected
- performance is improved
- documentation is updated
- mechanization exit‑code handling is updated

---

## 2. Schema Versioning

Schema versioning is **independent** of pipeline versioning.

### Schema Version Format

```json
schema_version: "1.1.1"
```

### Schema Version Bump Rules

- **MAJOR** — breaking column changes
- **MINOR** — new optional fields
- **PATCH** — corrections to descriptions or metadata

Schema version must appear in:

- `data/stage01_schema/schema.json`
- `manifest.provenance.schema_version`
- Stage 01 diagnostics
- Stage 03 drift checks

---

## 3. Artifact Versioning

Artifacts generated in Stage 04 must include deterministic version metadata.

### Artifact Version Format

```json
artifact_version: "1.1.1"
```

### Artifact Version Bump Rules

- **MAJOR** — breaking changes to artifact structure
- **MINOR** — new fields added
- **PATCH** — formatting or metadata fixes

Artifact version must appear in:

- `dataset_summary.json`
- `column_health.json`
- `pipeline_summary.json`
- artifact registry

---

## 4. Manifest Versioning

The manifest (`manifest.json` and `pipeline_summary.json`) includes its own version.

### Manifest Version Format

```json
manifest_version: "1.1.1"
```

### Manifest Version Bump Rules

- **MAJOR** — breaking changes to manifest structure
- **MINOR** — new fields added
- **PATCH** — metadata corrections

Manifest version must appear in:

- Stage 05 output
- provenance metadata
- CI/CD validation

---

## 5. Deployment Versioning

Deployment configurations (Dockerfile, Compose, Helm, Terraform) must include a
deterministic deployment version.

### Deployment Version Format

```json
deployment_version: "1.1.1"
```

### Deployment Version Bump Rules

- **MAJOR** — breaking changes to deployment topology
- **MINOR** — new deployment features
- **PATCH** — configuration fixes

Deployment version must appear in:

- Docker labels
- Helm chart annotations
- Terraform outputs
- CI/CD logs

### Deployment Components

Deployment versioning applies to:

- `deployment/Dockerfile`
- root‑level `compose.yml`
- `deployment/helm/Chart.yml`
- `deployment/terraform/main.tf`

---

## 6. Mechanization Versioning

Mechanization includes:

- C++ schema validator
- C++ row counter
- Python/C++ hybrid runners
- mechanization provenance fields

### Mechanization Version Format

```json
mechanization_version: "1.1.1"
```

### Mechanization Version Bump Rules

- **MAJOR** — new C++ validators, new mechanization semantics
- **MINOR** — new mechanization utilities
- **PATCH** — exit‑code fixes, logging fixes

Mechanization version must appear in:

- `manifest.provenance.mechanization_mode`
- `manifest.mechanization`
- Stage 05 summary

---

## 7. Provenance Versioning

Provenance metadata must include **all version layers**:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
mechanization_version
sbom_version
```

This ensures reproducibility across:

- local
- docker
- docker-compose
- CI/CD
- Kubernetes
- Helm
- cloud

---

## 8. Version Propagation Rules

Version changes must propagate deterministically:

### Pipeline → Manifest

Pipeline version must be written into:

- `pipeline_summary.json`
- provenance metadata

### Schema → Diagnostics

Schema version must be validated in:

- Stage 01 diagnostics
- Stage 03 quality checks

### Artifacts → Registry

Artifact version must be included in:

- `dataset_summary.json`
- `column_health.json`
- artifact registry

### Deployment → CI/CD

Deployment version must be logged in:

- GitHub Actions
- Docker labels
- Helm chart annotations

### Mechanization → Provenance

Mechanization version must be included in:

- mechanization metadata
- C++ exit‑code provenance
- Stage 05 summary

---

## 9. Reproducibility Contract

Versioning **must**:

- use pinned SemVer rules
- use pinned version fields
- avoid nondeterministic version bumps
- be validated in CI/CD
- be included in manifest.provenance
- be consistent across all layers
- be reproducible from a clean clone

This ensures versioning behaves identically across all environments.

---

## Future Extensions

- distributed ingestion versioning
- multi-region deployment versioning
- RAG/AI indexing versioning
- OpenTelemetry version propagation
- SBOM versioning
- mechanization performance versioning
