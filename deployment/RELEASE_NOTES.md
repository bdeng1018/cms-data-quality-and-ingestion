# CMS Data Quality & Ingestion Pipeline — Release Notes Contract

## Documentation Contract

This document defines the deterministic release notes structure for the CMS Data
Quality & Ingestion Pipeline. Release notes must track pipeline changes,
deployment changes, schema changes, artifact changes, manifest changes, and
observability changes in a reproducible and provenance-aware format.

### Determinism Guarantees

- stable release note structure  
- stable version bump rules  
- stable change categories  
- reproducible provenance fields  
- deterministic ordering  

### Side Effects

- documents pipeline evolution  
- documents schema evolution  
- documents artifact evolution  
- documents deployment evolution  
- documents observability evolution  

---

## Release Notes Structure (Deterministic)

Each release must follow the pinned structure:

```markdown
## [VERSION] — YYYY-MM-DD
### Added
### Changed
### Fixed
### Removed
### Deprecated
### Security
### Observability
### Provenance
```

This structure must never change without a **MAJOR** version bump.

---

## Version Bump Rules

Release notes must follow the versioning rules defined in
**[VERSIONING.md](ca://s?q=Show_VERSIONING_contract)**.

### MAJOR

Increment when:

- schema changes break compatibility  
- artifact formats change  
- manifest structure changes  
- pipeline execution semantics change  
- deployment topology changes  

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

## Change Categories (Deterministic)

### Added

New features, new metrics, new diagnostics, new artifacts, new deployment options.

### Changed

Modifications to existing behavior that do not break compatibility.

### Fixed

Bug fixes, diagnostics corrections, artifact formatting fixes.

### Removed

Deprecated or eliminated functionality.

### Deprecated

Features scheduled for removal in a future release.

### Security

Hardening changes, policy updates, vulnerability fixes.

### Observability

Metrics, alerts, dashboards, logging, tracing changes.

### Provenance

Changes to provenance fields, manifest structure, version propagation.

---

## Provenance Mapping

Each release note entry must include deterministic provenance fields:

```text
pipeline_version
schema_version
artifact_version
manifest_version
deployment_version
observability_version (future)
```

These fields ensure reproducibility across:

- local  
- docker-compose  
- Kubernetes  
- Helm  
- cloud  

---

## Example Release Note (Pinned Format)

```markdown
## 1.2.0 — 2026-07-31

### Added
- New ingestion latency SLOs.
- Added `cms_artifact_bytes_total` metric.

### Changed
- Updated schema descriptions for POS Q2 2026.

### Fixed
- Corrected diagnostics pass rate calculation.

### Removed
- Deprecated Stage 02 legacy ingestion path.

### Deprecated
- Old `facility_health.csv` format scheduled for removal in 1.3.0.

### Security
- Updated `HARDENING.md` with new PSP rules.

### Observability
- Added `OBSERVABILITY.md` contract.
- Updated Grafana dashboard panels.

### Provenance
- Updated `manifest.provenance` to include `deployment_version`.
```

---

## Reproducibility Contract

Release notes **must**:

- follow pinned structure  
- follow pinned version bump rules  
- avoid nondeterministic ordering  
- avoid nondeterministic categories  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures release documentation behaves identically across all environments.

---

## Future Extensions

- distributed ingestion release notes  
- multi-region deployment release notes  
- RAG/AI indexing release notes  
- SBOM release notes  
- OpenTelemetry release notes  
