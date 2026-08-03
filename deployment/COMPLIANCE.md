# CMS Data Quality & Ingestion Pipeline — Compliance Contract

## Documentation Contract

This document defines the deterministic compliance rules for the CMS Data Quality
& Ingestion Pipeline. Compliance ensures that pipeline behavior, schema handling,
artifact generation, deployment configuration, observability, and provenance
adhere to reproducible, auditable, and governance‑aligned standards.

### Determinism Guarantees

- stable compliance categories  
- pinned compliance requirements  
- reproducible auditability  
- deterministic provenance fields  
- consistent enforcement across environments  

### Side Effects

- enforces regulatory alignment  
- enforces governance alignment  
- enforces auditability  
- enforces versioning discipline  
- enforces deployment security  

---

## Compliance Categories (Deterministic)

Compliance is divided into pinned categories:

1. **Pipeline Compliance**  
2. **Schema Compliance**  
3. **Artifact Compliance**  
4. **Manifest Compliance**  
5. **Deployment Compliance**  
6. **Observability Compliance**  
7. **Security Compliance**  
8. **Provenance Compliance**  
9. **Audit Compliance**  
10. **SBOM Compliance**

Each category has deterministic rules and enforcement requirements.

---

## Pipeline Compliance

Pipeline execution must comply with:

- deterministic stage ordering  
- deterministic runtime SLOs  
- deterministic artifact generation  
- deterministic diagnostics  
- deterministic provenance updates  

Pipeline compliance requires:

- SBOM update  
- RELEASE_NOTES update  
- audit event generation  
- CI/CD validation  

---

## Schema Compliance

Schema handling must comply with:

- pinned schema versioning rules  
- deterministic compatibility rules  
- deterministic diagnostics validation  
- deterministic schema provenance  

### Schema Change Categories

- **MAJOR** — breaking column changes  
- **MINOR** — new optional fields  
- **PATCH** — metadata corrections  

Schema compliance requires:

- schema_version bump  
- SBOM update  
- audit event generation  
- RELEASE_NOTES update  

---

## Artifact Compliance

Artifact generation must comply with:

- pinned artifact versioning rules  
- deterministic artifact structure  
- deterministic artifact registry validation  
- deterministic artifact provenance  

### Artifact Change Categories

- **MAJOR** — breaking artifact structure changes  
- **MINOR** — new fields added  
- **PATCH** — formatting fixes  

Artifact compliance requires:

- artifact_version bump  
- SBOM update  
- audit event generation  
- RELEASE_NOTES update  

---

## Manifest Compliance

Manifests must comply with:

- pinned manifest versioning rules  
- deterministic manifest structure  
- deterministic provenance fields  
- deterministic ordering  

Manifest compliance requires:

- manifest_version bump  
- SBOM update  
- audit event generation  

---

## Deployment Compliance

Deployment configurations must comply with:

- pinned deployment versioning rules  
- deterministic Docker/Compose/Helm/Terraform rules  
- deterministic security posture  
- deterministic CI/CD validation  

### Deployment Components

Deployment compliance applies to:

- `deployment/Dockerfile`  
- root‑level `compose.yml`  
- `deployment/helm/Chart.yml`  
- `deployment/terraform/main.tf`  

Deployment compliance requires:

- deployment_version bump  
- SBOM update  
- audit event generation  
- RELEASE_NOTES update  

---

## Observability Compliance

Observability must comply with:

- pinned metric names  
- pinned alert thresholds  
- pinned dashboard panels  
- pinned log formats  
- deterministic provenance fields  

Observability compliance requires:

- SBOM update  
- audit event generation  
- RELEASE_NOTES update  

---

## Security Compliance

Security must comply with:

- pinned hardening rules  
- deterministic PSP/NetworkPolicy rules  
- deterministic container security rules  
- deterministic access control rules  

Security compliance requires:

- HARDENING.md alignment  
- audit event generation  
- SBOM update  

---

## Provenance Compliance

Provenance must include deterministic fields:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
observability_version (future)
sbom_version
```

Provenance compliance requires:

- provenance update  
- audit event generation  
- SBOM update  

---

## Audit Compliance

Audit logs must comply with:

- pinned audit event structure  
- deterministic categories  
- deterministic retention rules  
- deterministic ordering  

Audit compliance requires:

- AUDIT_LOGS.md alignment  
- CI/CD audit hooks  
- provenance update  

---

## SBOM Compliance

SBOMs must comply with:

- pinned SBOM structure  
- deterministic dependency inventory  
- pinned version fields  
- deterministic ordering  

SBOM compliance requires:

- SBOM version bump  
- audit event generation  
- RELEASE_NOTES update  

---

## Compliance Enforcement Workflow (Deterministic)

All compliance actions must follow the pinned workflow:

1. **Identify Compliance Requirement**  
2. **Apply Change**  
3. **Version Bump**  
4. **SBOM Update**  
5. **RELEASE_NOTES Update**  
6. **Audit Event Generation**  
7. **Provenance Update**  
8. **CI/CD Validation**  
9. **Merge to Main**  

This workflow must never change without a **MAJOR** version bump.

---

## Reproducibility Contract

Compliance **must**:

- follow pinned rules  
- follow pinned workflows  
- avoid nondeterministic enforcement  
- avoid nondeterministic versioning  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures compliance behaves identically across all environments.

---

## Future Extensions

- distributed ingestion compliance  
- multi-region compliance  
- RAG/AI indexing compliance  
- SBOM attestation compliance  
- OpenTelemetry compliance  
