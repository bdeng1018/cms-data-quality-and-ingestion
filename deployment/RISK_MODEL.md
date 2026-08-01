
# CMS Data Quality & Ingestion Pipeline — Risk Model Contract

## Documentation Contract

This document defines the deterministic risk model for the CMS Data Quality &
Ingestion Pipeline. The risk model ensures reproducible identification,
classification, mitigation, and provenance tracking of ingestion risks across all
pipeline layers.

### Determinism Guarantees

- stable risk categories  
- stable risk definitions  
- pinned severity levels  
- reproducible mitigation rules  
- deterministic provenance fields  

### Side Effects

- enforces ingestion stability  
- enforces schema stability  
- enforces artifact stability  
- enforces deployment stability  
- enforces observability stability  

---

## Risk Categories (Deterministic)

The pipeline uses pinned risk categories:

1. **Ingestion Risks**  
2. **Schema Risks**  
3. **Artifact Risks**  
4. **Manifest Risks**  
5. **Deployment Risks**  
6. **Observability Risks**  
7. **Provenance Risks**  

Each category has deterministic definitions and mitigation rules.

---

## Severity Levels (Pinned)

Severity levels must follow a deterministic scale:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Severity levels must never change without a **MAJOR** version bump.

---

## Ingestion Risks

### Risk: Source Data Missing

- **Severity:** HIGH  
- **Description:** Required POS/QIES files missing or inaccessible.  
- **Mitigation:**  
  - validate source paths  
  - enforce CI/CD ingestion checks  
  - update provenance fields  

### Risk: Ingestion Latency Regression

- **Severity:** MEDIUM  
- **Description:** Pipeline runtime exceeds SLO.  
- **Mitigation:**  
  - monitor `cms_pipeline_runtime_seconds`  
  - enforce SLO thresholds  
  - update RELEASE_NOTES  

---

## Schema Risks

### Risk: Breaking Schema Change

- **Severity:** CRITICAL  
- **Description:** Column changes break compatibility.  
- **Mitigation:**  
  - bump schema_version  
  - update SBOM  
  - update RELEASE_NOTES  
  - update manifest.provenance  

### Risk: Schema Drift

- **Severity:** HIGH  
- **Description:** Schema does not match actual data.  
- **Mitigation:**  
  - run Stage 01 diagnostics  
  - enforce schema loader validation  

---

## Artifact Risks

### Risk: Artifact Format Change

- **Severity:** CRITICAL  
- **Description:** Artifact structure changes unexpectedly.  
- **Mitigation:**  
  - bump artifact_version  
  - update SBOM  
  - update RELEASE_NOTES  

### Risk: Artifact Missing

- **Severity:** HIGH  
- **Description:** Expected Stage 04 artifacts not generated.  
- **Mitigation:**  
  - enforce artifact registry validation  
  - monitor `cms_pipeline_artifacts_generated_total`  

---

## Manifest Risks

### Risk: Manifest Structure Change

- **Severity:** CRITICAL  
- **Description:** Manifest fields change unexpectedly.  
- **Mitigation:**  
  - bump manifest_version  
  - update SBOM  
  - update RELEASE_NOTES  

### Risk: Provenance Incomplete

- **Severity:** HIGH  
- **Description:** Missing version fields in manifest.  
- **Mitigation:**  
  - enforce Stage 05 validation  
  - update provenance fields  

---

## Deployment Risks

### Risk: Deployment Drift

- **Severity:** HIGH  
- **Description:** Deployment configuration diverges from repo.  
- **Mitigation:**  
  - enforce Terraform plan checks  
  - enforce Helm diff checks  

### Risk: Container Misconfiguration

- **Severity:** CRITICAL  
- **Description:** Container runs with elevated privileges.  
- **Mitigation:**  
  - enforce HARDENING.md rules  
  - enforce PSP/NetworkPolicy  

---

## Observability Risks

### Risk: Metrics Missing

- **Severity:** HIGH  
- **Description:** Metrics not emitted or scraped.  
- **Mitigation:**  
  - validate Prometheus targets  
  - enforce METRICS.md contract  

### Risk: Alerts Not Firing

- **Severity:** CRITICAL  
- **Description:** Alert thresholds misconfigured.  
- **Mitigation:**  
  - validate alert rules  
  - enforce ALERTS contract  

---

## Provenance Risks

### Risk: Version Mismatch

- **Severity:** CRITICAL  
- **Description:** Version fields inconsistent across layers.  
- **Mitigation:**  
  - enforce VERSIONING.md  
  - enforce manifest.provenance  

### Risk: Missing Provenance Fields

- **Severity:** HIGH  
- **Description:** Provenance incomplete or missing.  
- **Mitigation:**  
  - enforce Stage 05 validation  
  - update SBOM  

---

## Risk Mitigation Workflow (Deterministic)

All risks must follow the pinned workflow:

1. **Identify Risk**  
2. **Classify Severity**  
3. **Apply Mitigation**  
4. **Update SBOM**  
5. **Update RELEASE_NOTES**  
6. **Update Provenance**  
7. **Validate in CI/CD**  
8. **Merge to Main**  

This workflow must never change without a **MAJOR** version bump.

---

## Reproducibility Contract

Risk modeling **must**:

- follow pinned categories  
- follow pinned severity levels  
- avoid nondeterministic classification  
- avoid nondeterministic mitigation  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures risk modeling behaves identically across all environments.

---

## Future Extensions

- distributed ingestion risk model  
- multi-region risk model  
- RAG/AI indexing risk model  
- SBOM attestation risk model  
- OpenTelemetry risk model  
