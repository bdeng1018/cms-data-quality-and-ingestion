# Deployment Layer Overview

The `deployment/` directory defines the runtime architecture for the CMS Data
Quality & Ingestion Pipeline. It provides deterministic, reproducible deployment
behavior across local development, docker-compose, Kubernetes, Helm packaging,
and Terraform-managed infrastructure.

This README serves as a navigation index for the deployment subsystem.

---

## 1. Deployment Contracts

Core deployment contracts live at the root of this directory:

- `DEPLOYMENT.md` — runtime architecture and deployment model  
- `OPERATIONS.md` — operational rules and runtime behavior  
- `CONTRACTS.md` — deterministic deployment contracts  
- `MANIFEST_SPEC.md` — manifest + provenance specification  
- `SBOM.md` — software bill of materials  
- `VERSIONING.md` — versioning rules  
- `GOVERNANCE.md` — governance rules  
- `COMPLIANCE.md` — compliance requirements  
- `RISK_MODEL.md` — risk classification  
- `AUDIT_LOGS.md` — audit log structure  
- `ACCESS_CONTROL.md` — RBAC and permission boundaries  

These documents define how deployment behaves across all environments.

---

## 2. Subsystem Map

The deployment layer is organized into subsystem directories:

```text
deployment/
  ci/            # CI/CD workflows and validation
  env/           # environment variable definitions
  helm/          # Helm chart and values
  k8s/           # Kubernetes manifests
  terraform/     # infrastructure provisioning
  logging/       # logging configuration
  monitoring/    # metrics, alerts, dashboards
  security/      # hardening and security policies
```

Each subsystem maps to a specific part of the runtime architecture.

---

## 3. CI/CD

`ci/` contains GitHub Actions workflows and validation rules.

Key responsibilities:

- pipeline execution  
- SBOM validation  
- provenance validation  
- release notes validation  
- audit log generation  

---

## 4. Environment Configuration

`env/` defines deterministic environment variable sets:

- `dev.env`  
- `prod.env`  

These files provide reproducible environment boundaries.

---

## 5. Containerization & Orchestration

### docker-compose  

Defined in `compose.yml` for local development.

### Kubernetes  

Raw manifests live in `k8s/`:

- `deployment.yml`  
- `service.yml`  

### Helm  

Packaged deployment lives in `helm/`:

- `Chart.yml`  
- `values.yml`  

---

## 6. Infrastructure Provisioning

`terraform/` defines infrastructure provisioning and drift detection:

- `main.tf`  
- `variables.tf`  
- `outputs.tf`  

Terraform ensures reproducible infrastructure across environments.

---

## 7. Logging & Monitoring

### Logging  

`logging/` contains Fluent Bit configuration and log routing.

### Monitoring  

`monitoring/` includes:

- Prometheus config  
- Grafana dashboard  
- alert rules  
- SLO/SLI contracts  
- observability rules  

---

## 8. Security

`security/` contains:

- `HARDENING.md` — container + runtime hardening  
- `policies.yml` — security policies and RBAC alignment  

Security integrates with governance, compliance, and access control.

---

## 9. How Deployment Integrates with the Pipeline

Deployment integrates with the pipeline through:

- containerized stage execution  
- Kubernetes/Helm orchestration  
- Terraform infrastructure  
- SBOM + provenance tracking  
- CI/CD validation  
- audit logging  
- governance + compliance enforcement  

This ensures deterministic, reproducible behavior across all environments.

---

## 10. Maintainer

Maintainer: Brian Deng  
Email: <bdeng.data.pipelines@gmail.com>  
GitHub: <https://github.com/bdeng1018>
