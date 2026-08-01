
# CMS Data Quality & Ingestion Pipeline — Incident Response Contract

## Documentation Contract

This document defines the deterministic incident response (IR) workflow for the
CMS Data Quality & Ingestion Pipeline. Incident response ensures reproducible
handling of ingestion failures, schema breaks, artifact corruption, manifest
errors, deployment outages, observability failures, and provenance inconsistencies.

### Determinism Guarantees

- stable IR workflow  
- pinned incident categories  
- reproducible severity levels  
- deterministic escalation rules  
- consistent CI/CD enforcement  

### Side Effects

- enforces operational stability  
- enforces governance compliance  
- enforces audit completeness  
- enforces provenance correctness  
- enforces deployment reliability  

---

## Incident Categories (Deterministic)

Incidents fall into pinned categories:

1. **Ingestion Incidents**  
2. **Schema Incidents**  
3. **Artifact Incidents**  
4. **Manifest Incidents**  
5. **Deployment Incidents**  
6. **Observability Incidents**  
7. **Security Incidents**  
8. **Provenance Incidents**

Each category has deterministic handling rules.

---

## Severity Levels (Pinned)

Severity levels must follow the deterministic scale:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Severity levels must never change without a **MAJOR** version bump.

---

## Ingestion Incidents

### Incident: Source Data Missing

- **Severity:** HIGH  
- **Description:** Required POS/QIES files missing.  
- **Immediate Actions:**  
  - validate source paths  
  - check ingestion logs  
  - notify pipeline operator  
- **Follow‑Up:**  
  - update RELEASE_NOTES  
  - generate audit event  
  - update provenance  

### Incident: Ingestion Latency Regression

- **Severity:** MEDIUM  
- **Description:** Pipeline runtime exceeds SLO.  
- **Immediate Actions:**  
  - inspect runtime metrics  
  - validate resource allocation  
- **Follow‑Up:**  
  - update SLO_SLI.md  
  - generate audit event  

---

## Schema Incidents

### Incident: Schema Mismatch

- **Severity:** CRITICAL  
- **Description:** Data does not match schema.  
- **Immediate Actions:**  
  - run Stage 01 diagnostics  
  - identify breaking column  
- **Follow‑Up:**  
  - bump schema_version  
  - update SBOM  
  - update RELEASE_NOTES  
  - generate audit event  

### Incident: Schema Drift

- **Severity:** HIGH  
- **Description:** Schema diverges from actual data.  
- **Immediate Actions:**  
  - validate schema loader  
  - inspect raw data  
- **Follow‑Up:**  
  - update schema definition  
  - update provenance  

---

## Artifact Incidents

### Incident: Artifact Missing

- **Severity:** HIGH  
- **Description:** Expected Stage 04 artifact not generated.  
- **Immediate Actions:**  
  - inspect reporting logs  
  - validate artifact registry  
- **Follow‑Up:**  
  - update RELEASE_NOTES  
  - generate audit event  

### Incident: Artifact Corruption

- **Severity:** CRITICAL  
- **Description:** Artifact structure invalid or unreadable.  
- **Immediate Actions:**  
  - validate artifact format  
  - inspect Stage 04 output  
- **Follow‑Up:**  
  - bump artifact_version  
  - update SBOM  
  - update provenance  

---

## Manifest Incidents

### Incident: Manifest Write Failure

- **Severity:** CRITICAL  
- **Description:** Manifest not written or incomplete.  
- **Immediate Actions:**  
  - inspect Stage 05 logs  
  - validate manifest path  
- **Follow‑Up:**  
  - update manifest_version  
  - generate audit event  

### Incident: Provenance Incomplete

- **Severity:** HIGH  
- **Description:** Missing version fields.  
- **Immediate Actions:**  
  - validate provenance writer  
- **Follow‑Up:**  
  - update provenance  
  - update SBOM  

---

## Deployment Incidents

### Incident: Deployment Drift

- **Severity:** HIGH  
- **Description:** Deployment config diverges from repo.  
- **Immediate Actions:**  
  - run Terraform plan  
  - run Helm diff  
- **Follow‑Up:**  
  - update RELEASE_NOTES  
  - generate audit event  

### Incident: Container Misconfiguration

- **Severity:** CRITICAL  
- **Description:** Container runs with elevated privileges.  
- **Immediate Actions:**  
  - enforce HARDENING.md  
  - validate PSP/NetworkPolicy  
- **Follow‑Up:**  
  - update security policies  
  - update SBOM  

---

## Observability Incidents

### Incident: Metrics Missing

- **Severity:** HIGH  
- **Description:** Metrics not emitted or scraped.  
- **Immediate Actions:**  
  - validate Prometheus targets  
  - inspect exporter logs  
- **Follow‑Up:**  
  - update METRICS.md  
  - generate audit event  

### Incident: Alerts Not Firing

- **Severity:** CRITICAL  
- **Description:** Alert thresholds misconfigured.  
- **Immediate Actions:**  
  - validate alert rules  
  - inspect Prometheus logs  
- **Follow‑Up:**  
  - update alerts.yml  
  - update RELEASE_NOTES  

---

## Security Incidents

### Incident: Policy Violation

- **Severity:** CRITICAL  
- **Description:** Security policy violated.  
- **Immediate Actions:**  
  - enforce HARDENING.md  
  - validate policies.yml  
- **Follow‑Up:**  
  - generate audit event  
  - update COMPLIANCE.md  

---

## Provenance Incidents

### Incident: Version Mismatch

- **Severity:** CRITICAL  
- **Description:** Version fields inconsistent across layers.  
- **Immediate Actions:**  
  - validate manifest.provenance  
- **Follow‑Up:**  
  - update SBOM  
  - update RELEASE_NOTES  

---

## Incident Response Workflow (Deterministic)

All incidents must follow the pinned workflow:

1. **Detect Incident**  
2. **Classify Severity**  
3. **Contain Impact**  
4. **Apply Immediate Actions**  
5. **Generate Audit Event**  
6. **Apply Follow‑Up Actions**  
7. **Update SBOM**  
8. **Update RELEASE_NOTES**  
9. **Update Provenance**  
10. **Validate in CI/CD**  
11. **Close Incident**  

This workflow must never change without a **MAJOR** version bump.

---

## Reproducibility Contract

Incident response **must**:

- follow pinned categories  
- follow pinned severity levels  
- avoid nondeterministic actions  
- avoid nondeterministic escalation  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures incident response behaves identically across all environments.

---

## Future Extensions

- distributed ingestion IR  
- multi-region IR  
- RAG/AI indexing IR  
- SBOM attestation IR  
- OpenTelemetry IR  
