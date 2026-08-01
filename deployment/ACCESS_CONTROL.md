
# CMS Data Quality & Ingestion Pipeline — Access Control Contract

## Documentation Contract

This document defines the deterministic access control rules for the CMS Data
Quality & Ingestion Pipeline. Access control ensures least‑privilege operation,
role separation, auditability, and reproducible permission boundaries across all
pipeline layers.

### Determinism Guarantees

- stable RBAC structure  
- pinned role definitions  
- reproducible permission boundaries  
- deterministic auditability  
- consistent enforcement across environments  

### Side Effects

- enforces least privilege  
- enforces governance compliance  
- enforces audit compliance  
- enforces deployment security  
- enforces provenance completeness  

---

## RBAC Model (Deterministic)

The pipeline uses a pinned RBAC model with deterministic roles:

1. **Pipeline Operator**  
2. **Data Engineer**  
3. **Quality Engineer**  
4. **Deployment Engineer**  
5. **Security Engineer**  
6. **Compliance Officer**  
7. **Auditor**  

Each role has pinned permissions and deterministic boundaries.

---

## Role Definitions

### **Pipeline Operator**

- run pipeline  
- view logs  
- view artifacts  
- no schema modification  
- no deployment modification  

### **Data Engineer**

- modify ingestion logic  
- modify schema loader  
- modify cleaning logic  
- view diagnostics  
- no deployment modification  

### **Quality Engineer**

- modify quality checks  
- modify quality engine  
- modify quality diagnostics  
- view artifacts  
- no ingestion modification  

### **Deployment Engineer**

- modify Dockerfile  
- modify Compose  
- modify Helm  
- modify Terraform  
- no schema modification  

### **Security Engineer**

- modify HARDENING.md  
- modify security policies  
- modify PSP/NetworkPolicy  
- modify access rules  
- no ingestion modification  

### **Compliance Officer**

- modify COMPLIANCE.md  
- modify GOVERNANCE.md  
- modify RISK_MODEL.md  
- modify AUDIT_LOGS.md  
- no pipeline logic modification  

### **Auditor**

- read‑only access to:  
  - logs  
  - audit logs  
  - SBOM  
  - manifests  
  - release notes  
- no write access  

---

## Permission Boundaries (Deterministic)

Permission boundaries must follow pinned rules:

```text
read_only
read_write
admin
```

Boundaries must never change without a **MAJOR** version bump.

---

## Access Control Enforcement

Access control must be enforced at:

- pipeline entrypoint  
- schema loader  
- quality engine  
- reporting engine  
- manifest writer  
- deployment subsystem  
- observability subsystem  
- CI/CD  

Enforcement must be deterministic across:

- local  
- docker-compose  
- Kubernetes  
- Helm  
- cloud  

---

## Access Control Provenance

Access control changes must generate audit events with pinned fields:

```text
actor
role
timestamp
change_type
component
provenance:
  pipeline_version
  schema_version
  artifact_version
  manifest_version
  deployment_version
  sbom_version
```

---

## Access Control Workflow (Deterministic)

All access control changes must follow the pinned workflow:

1. **Propose Change**  
2. **Governance Review**  
3. **Security Review**  
4. **Compliance Review**  
5. **Audit Event Generation**  
6. **Version Bump (if required)**  
7. **SBOM Update**  
8. **RELEASE_NOTES Update**  
9. **Merge to Main**  

This workflow must never change without a **MAJOR** version bump.

---

## Reproducibility Contract

Access control **must**:

- follow pinned RBAC rules  
- follow pinned permission boundaries  
- avoid nondeterministic role changes  
- avoid nondeterministic enforcement  
- be validated in CI/CD  
- be included in manifest.provenance  

This ensures access control behaves identically across all environments.

---

## Future Extensions

- IAM integration  
- OIDC integration  
- signed access control policies  
- multi-region access control  
- distributed ingestion access control
