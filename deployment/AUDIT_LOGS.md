
# CMS Data Quality & Ingestion Pipeline — Audit Logs Contract

## Documentation Contract

This document defines the deterministic audit logging rules for the CMS Data
Quality & Ingestion Pipeline. Audit logs provide reproducible tracking of changes
across pipeline execution, schema evolution, artifact generation, manifest
updates, deployment changes, observability changes, and governance actions.

### Determinism Guarantees

- stable audit log structure  
- stable audit event categories  
- pinned provenance fields  
- reproducible ordering  
- deterministic retention rules  

### Side Effects

- enforces governance compliance  
- enforces versioning compliance  
- enforces release compliance  
- enforces provenance compliance  
- enforces deployment compliance  

---

## Audit Log Structure (Deterministic)

Audit logs must follow the pinned structure:

```text
timestamp
event_type
actor
component
description
provenance:
  pipeline_version
  schema_version
  artifact_version
  manifest_version
  deployment_version
  observability_version (future)
```

This structure must never change without a **MAJOR** version bump.

---

## Audit Event Categories (Pinned)

Audit events fall into deterministic categories:

1. **Pipeline Events**  
2. **Schema Events**  
3. **Artifact Events**  
4. **Manifest Events**  
5. **Deployment Events**  
6. **Observability Events**  
7. **Governance Events**  
8. **Versioning Events**  
9. **Release Events**  
10. **Provenance Events**

Each category has pinned semantics.

---

## Pipeline Audit Events

### Event: Pipeline Execution Started

- **Component:** stage05_pipeline_runner  
- **Description:** Pipeline execution initiated.  
- **Provenance:** pipeline_version required.

### Event: Pipeline Execution Completed

- **Component:** stage05_pipeline_runner  
- **Description:** Pipeline execution completed.  
- **Provenance:** pipeline_version required.

---

## Schema Audit Events

### Event: Schema Version Bumped

- **Component:** stage01_schema_definition  
- **Description:** Schema version incremented.  
- **Provenance:** schema_version required.

### Event: Schema Diagnostics Failed

- **Component:** stage01 diagnostics  
- **Description:** Schema mismatch detected.  
- **Provenance:** schema_version required.

---

## Artifact Audit Events

### Event: Artifact Generated

- **Component:** stage04_reporting  
- **Description:** Artifact successfully generated.  
- **Provenance:** artifact_version required.

### Event: Artifact Missing

- **Component:** stage04_reporting  
- **Description:** Expected artifact not generated.  
- **Provenance:** artifact_version required.

---

## Manifest Audit Events

### Event: Manifest Written

- **Component:** stage05_pipeline_runner  
- **Description:** Manifest successfully written.  
- **Provenance:** manifest_version required.

### Event: Manifest Provenance Updated

- **Component:** stage05_pipeline_runner  
- **Description:** Provenance fields updated.  
- **Provenance:** all version fields required.

---

## Deployment Audit Events

### Event: Deployment Version Bumped

- **Component:** deployment subsystem  
- **Description:** Deployment version incremented.  
- **Provenance:** deployment_version required.

### Event: Deployment Drift Detected

- **Component:** CI/CD  
- **Description:** Deployment configuration mismatch.  
- **Provenance:** deployment_version required.

---

## Observability Audit Events

### Event: Metrics Updated

- **Component:** monitoring subsystem  
- **Description:** Metrics contract updated.  
- **Provenance:** observability_version required (future).

### Event: Alerts Updated

- **Component:** monitoring subsystem  
- **Description:** Alert thresholds updated.  
- **Provenance:** observability_version required (future).

---

## Governance Audit Events

### Event: Governance Rule Updated

- **Component:** governance subsystem  
- **Description:** Governance rule modified.  
- **Provenance:** pipeline_version required.

### Event: Approval Workflow Executed

- **Component:** governance subsystem  
- **Description:** Change approved via deterministic workflow.  
- **Provenance:** all version fields required.

---

## Versioning Audit Events

### Event: Version Bump

- **Component:** versioning subsystem  
- **Description:** Version increment applied.  
- **Provenance:** version fields required.

---

## Release Audit Events

### Event: Release Created

- **Component:** release subsystem  
- **Description:** Release created following deterministic structure.  
- **Provenance:** all version fields required.

### Event: Release Notes Updated

- **Component:** release subsystem  
- **Description:** Release notes updated.  
- **Provenance:** pipeline_version required.

---

## Provenance Audit Events

### Event: Provenance Updated

- **Component:** stage05_pipeline_runner  
- **Description:** Provenance fields updated.  
- **Provenance:** all version fields required.

---

## Audit Log Retention Rules (Deterministic)

Audit logs must follow pinned retention rules:

```text
minimum_retention: 365 days
maximum_retention: 1825 days
rotation_interval: 24 hours
rotation_format: audit-YYYY-MM-DD.log
```

Retention rules must never change without a **MAJOR** version bump.

---

## CI/CD Audit Hooks

CI/CD must generate audit events for:

- version bumps  
- releases  
- SBOM updates  
- governance approvals  
- deployment changes  
- manifest updates  
- schema updates  
- artifact generation  

Audit logs must be stored in:

```text
logs/audit/
```

---

## Reproducibility Contract

Audit logging **must**:

- follow pinned structure  
- follow pinned categories  
- avoid nondeterministic ordering  
- avoid nondeterministic retention  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures audit logging behaves identically across all environments.

---

## Future Extensions

- signed audit logs  
- tamper-evident audit logs  
- distributed audit logs  
- multi-region audit logs  
- SBOM attestation audit logs  
- OpenTelemetry audit logs  
