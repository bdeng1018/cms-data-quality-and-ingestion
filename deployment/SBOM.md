# CMS Data Quality & Ingestion Pipeline — SBOM Contract

## Documentation Contract

This document defines the deterministic Software Bill of Materials (SBOM)
structure for the CMS Data Quality & Ingestion Pipeline. The SBOM provides a
reproducible inventory of all dependencies, versions, artifacts, schemas,
manifests, and deployment components.

### Determinism Guarantees

- stable SBOM structure  
- stable dependency inventory  
- pinned versions  
- reproducible provenance fields  
- deterministic ordering  

### Side Effects

- documents dependency evolution  
- documents artifact evolution  
- documents schema evolution  
- documents deployment evolution  
- documents observability evolution  

---

## SBOM Structure (Deterministic)

Each SBOM must follow the pinned structure:

```markdown
## SBOM — [VERSION]
### Pipeline
### Dependencies
### Artifacts
### Schemas
### Manifests
### Deployment
### Observability
### Provenance
```

This structure must never change without a **MAJOR** version bump.

---

## Pipeline Section

The pipeline section must include:

- pipeline_version  
- pipeline entrypoint  
- pipeline stages  
- pipeline execution semantics  

Example:

```yaml
pipeline_version: 1.2.0
entrypoint: src/stage05_pipeline_runner/run_pipeline.py
stages:
  - stage01_schema_definition
  - stage02_raw_ingestion
  - stage03_data_quality
  - stage04_reporting
  - stage05_pipeline_runner
```

---

## Dependencies Section

Dependencies must be listed with:

- name  
- version  
- source  
- hash (future)  

Example:

```yaml
dependencies:
  - python: 3.11.4
  - pandas: 2.2.2
  - pyarrow: 16.1.0
  - pydantic: 2.7.1
  - uv: 0.1.0
```

Dependencies must match:

- `uv.lock`  
- `environment.yml`  
- CI/CD installation logs  

---

## Artifacts Section

Artifacts must include:

- artifact_version  
- artifact list  
- artifact sizes  
- artifact hashes (future)  

Example:

```yaml
artifacts:
  - dataset_summary.json
  - facility_health.csv
  - column_health.json
  - report_index.json
```

Artifact version must match:

- Stage 04 output  
- manifest.provenance  

---

## Schemas Section

Schemas must include:

- schema_version  
- schema file path  
- schema hash (future)  

Example:

```yaml
schemas:
  - stage01_schema/schema.json (v1.0.0)
```

Schema version must match:

- Stage 01 diagnostics  
- manifest.provenance  

---

## Manifests Section

Manifests must include:

- manifest_version  
- manifest file path  
- manifest structure hash (future)  

Example:

```yaml
manifests:
  - pipeline_summary.json (v1.2.0)
```

Manifest version must match:

- Stage 05 output  
- provenance metadata  

---

## Deployment Section

Deployment components must include:

- deployment_version  
- Dockerfile hash (future)  
- Compose version  
- Helm chart version  
- Terraform version  

Example:

```yaml
deployment:
  dockerfile: deployment/Dockerfile
  compose: compose.yml
  helm_chart: deployment/helm/Chart.yml
  terraform: deployment/terraform/main.tf
```

Deployment version must match:

- CI/CD logs  
- manifest.provenance  

---

## Observability Section

Observability components must include:

- metrics version  
- alerts version  
- dashboards version  
- logging version  

Example:

```yaml
observability:
  metrics: METRICS.md
  alerts: alerts.yml
  dashboards: grafana-dashboard.json
  logging: fluent-bit.conf
```

---

## Provenance Section

Each SBOM must include deterministic provenance fields:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
observability_version (future)
sbom_version
```

SBOM version must increment when:

- dependency inventory changes  
- schema changes  
- artifact formats change  
- manifest structure changes  
- deployment topology changes  

---

## Reproducibility Contract

SBOMs **must**:

- follow pinned structure  
- follow pinned version bump rules  
- avoid nondeterministic ordering  
- avoid nondeterministic categories  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures SBOM behavior is identical across all environments.

---

## Future Extensions

- SBOM hashing  
- SBOM signing (cosign)  
- SBOM attestation (in-toto)  
- distributed ingestion SBOMs  
- multi-region SBOMs  
- RAG/AI indexing SBOMs  
