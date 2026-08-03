# CMS Data Quality & Ingestion Pipeline — Versioning Contract

## Documentation Contract

This document defines the deterministic versioning rules for the CMS Data Quality
& Ingestion Pipeline. Versioning applies to pipeline releases, schemas, artifacts,
manifests, deployment configurations, and provenance metadata.

### Determinism Guarantees

- pinned semantic versioning rules  
- pinned schema versioning  
- pinned artifact versioning  
- pinned manifest versioning  
- pinned deployment versioning  
- reproducible version propagation  

### Side Effects

- enforces reproducible pipeline behavior  
- enforces deterministic artifact generation  
- enforces stable schema evolution  
- enforces consistent deployment upgrades  

---

## Semantic Versioning (Pipeline)

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

### MINOR

Increment when:

- new features are added  
- new metrics or diagnostics are added  
- new artifacts are added  
- new deployment options are added  

### PATCH

Increment when:

- bugs are fixed  
- diagnostics are corrected  
- performance is improved  
- documentation is updated  

---

## Schema Versioning

Schema versioning is **independent** of pipeline versioning.

### Schema Version Format

```json
schema_version: "1.0.0"
```

### Schema Version Bump Rules

- **MAJOR** — breaking column changes  
- **MINOR** — new optional fields  
- **PATCH** — corrections to descriptions or metadata  

Schema version must appear in:

- `data/stage01_schema/schema.json`  
- `manifest.provenance.schema_version`  
- Stage 01 diagnostics  

---

## Artifact Versioning

Artifacts generated in Stage 04 must include deterministic version metadata.

### Artifact Version Format

```json
artifact_version: "1.0.0"
```

### Artifact Version Bump Rules

- **MAJOR** — breaking changes to artifact structure  
- **MINOR** — new fields added  
- **PATCH** — formatting or metadata fixes  

Artifact version must appear in:

- `report_index.json`  
- `pipeline_summary.json`  
- artifact registry  

---

## Manifest Versioning

The manifest (`pipeline_summary.json`) includes its own version.

### Manifest Version Format

```json
manifest_version: "1.0.0"
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

## Deployment Versioning

Deployment configurations (Dockerfile, Compose, Helm, Terraform) must include a
deterministic deployment version.

### Deployment Version Format

```json
deployment_version: "1.0.0"
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

## Provenance Versioning

Provenance metadata must include **all version layers**:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
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

## Version Propagation Rules

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

- `report_index.json`  
- artifact registry  

### Deployment → CI/CD

Deployment version must be logged in:

- GitHub Actions  
- Docker labels  
- Helm chart annotations  

---

## Reproducibility Contract

Versioning **must**:

- use pinned SemVer rules  
- use pinned version fields  
- avoid nondeterministic version bumps  
- be validated in CI/CD  
- be included in manifest.provenance  
- be consistent across all layers  

This ensures versioning behaves identically across all environments.

---

## Future Extensions

- distributed ingestion versioning  
- multi-region deployment versioning  
- RAG/AI indexing versioning  
- OpenTelemetry version propagation  
- SBOM versioning  
