# CMS Data Quality & Ingestion Pipeline — Security Hardening Guide

## Documentation Contract

This guide defines the deterministic security hardening rules for the CMS
ingestion pipeline across Docker, Kubernetes, Helm, Terraform, and CI/CD layers.

### Determinism Guarantees

- stable security posture  
- pinned versions for all dependencies  
- reproducible container behavior  
- reproducible infra access patterns  

### Side Effects

- enforces least privilege  
- restricts container capabilities  
- restricts network exposure  
- enforces reproducible secrets handling  

---

## Container Security Hardening

### Principles

- containers must run as non‑root  
- containers must use read‑only root filesystem  
- containers must drop all Linux capabilities  
- writable mounts must be explicitly declared  
- no shell access inside production containers  

### Deterministic Contract

- `USER 1000:1000` in Dockerfile  
- `readOnlyRootFilesystem: true` in K8s  
- `securityContext.capabilities.drop: ["ALL"]`  
- `allowPrivilegeEscalation: false`  

---

## Secrets Management

### Principles

- secrets must never be stored in repo  
- secrets must never be stored in Docker images  
- secrets must be injected deterministically via environment or secret stores  

### Deterministic Contract

- GitHub Actions uses `secrets.*`  
- Kubernetes uses `Secret` objects  
- Terraform uses `sensitive = true` variables  
- no dynamic secret generation  

---

## Network Hardening

### Principles

- pipeline must not expose public ports unless required  
- ingress must be explicitly declared  
- egress must be restricted  

### Deterministic Contract

- K8s `NetworkPolicy` restricts ingress/egress  
- Terraform security groups pinned to known CIDRs  
- no wildcard `0.0.0.0/0` unless explicitly documented  

---

## Artifact + Log Hardening

### Principles

- artifacts must be immutable  
- logs must be append‑only  
- artifact registry must be validated  

### Deterministic Contract

- S3 bucket versioning enabled  
- artifact registry validated in CI/CD  
- logs stored in write‑only directories  

---

## CI/CD Hardening

### Principles

- CI/CD must not run untrusted code  
- CI/CD must not expose secrets  
- CI/CD must validate manifests + artifacts  

### Deterministic Contract

- pinned Python version  
- pinned uv.lock dependencies  
- deterministic validation steps  
- no dynamic job generation  

---

## Future Extensions

- OPA policy enforcement  
- Snyk/Trivy vulnerability scanning  
- SBOM generation  
- container signing (cosign)  
- Terraform drift detection  
- K8s admission controller policies  
