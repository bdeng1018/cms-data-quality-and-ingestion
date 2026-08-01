# CMS Data Quality & Ingestion Pipeline — Terraform Provisioning Layer

## Documentation Contract

This README defines the deterministic infrastructure provisioning rules for the
CMS Data Quality & Ingestion Pipeline. It describes how Terraform modules map to
pipeline reproducibility guarantees, artifact isolation, provenance tracking, and
deployment contracts.

### Determinism Guarantees

- Pinned provider versions  
- Pinned AMI + instance type  
- Stable bucket naming  
- Reproducible compute + storage configuration  
- Stable outputs for manifest.provenance  

### Side Effects

- Creates compute instance(s)  
- Creates storage buckets  
- Creates networking resources  
- Produces infra metadata consumed by pipeline runners  

---

## Overview

The Terraform module provisions deterministic infrastructure for the CMS Data
Quality & Ingestion Pipeline. It mirrors docker-compose and Kubernetes deployment
contracts while enabling cloud-based reproducible execution.

This provisioning layer is designed to be:

- deterministic  
- reproducible  
- contract-driven  
- environment‑agnostic  
- provenance‑aware  

---

## Directory Structure

```code
deployment/terraform/
    main.tf
    variables.tf
    outputs.tf
    README.md
```

Each file corresponds to a specific deployment contract:

- `main.tf` — compute, storage, networking  
- `variables.tf` — deterministic configuration inputs  
- `outputs.tf` — reproducible infra metadata  
- `README.md` — operational + reproducibility documentation  

---

## Provisioning Workflow (Deterministic)

### Initialization

```bash
terraform init
```

### Validation

```bash
terraform validate
```

### Apply Infrastructure

```bash
terraform apply
```

### Inspect Outputs

```bash
terraform output
```

Outputs include:

- EC2 instance ID  
- public IP  
- S3 bucket name  
- security group ID  

These map directly to `manifest.provenance`.

---

## Variables (Deterministic Inputs)

Defined in `variables.tf`:

| Variable        | Description                                 |
|-----------------|---------------------------------------------|
| `region`        | AWS region for deployment                   |
| `ami_id`        | pinned AMI for deterministic execution      |
| `instance_type` | pinned compute instance type                |
| `bucket_name`   | artifact + log storage bucket               |

These variables must remain stable across environments to preserve reproducibility.

---

## Outputs (Provenance Metadata)

Defined in `outputs.tf`:

| Output                        | Description                                  |
|-------------------------------|----------------------------------------------|
| `cms_pipeline_instance_id`    | deterministic compute runner                 |
| `cms_pipeline_public_ip`      | optional public endpoint                     |
| `cms_artifacts_bucket`        | artifact + log storage                       |
| `cms_pipeline_security_group` | networking contract                          |

These outputs are consumed by:

- pipeline runners  
- CI/CD workflows  
- manifest generation  
- provenance tracking  

---

## Reproducibility Contract

Terraform provisioning **must**:

- use pinned provider versions  
- use pinned AMI  
- use pinned instance type  
- produce stable outputs  
- avoid nondeterministic resource naming  
- maintain deterministic directory structure  
- preserve artifact isolation  

These rules ensure that infrastructure behaves identically across:

- local development  
- docker-compose  
- Kubernetes  
- Helm  
- CI/CD  
- cloud deployment  

---

## Future Extensions

This Terraform module is designed to evolve into a full ingestion platform:

- autoscaling  
- cloud ingestion endpoints  
- distributed ingestion cluster  
- multi-region ingestion  
- K8s + Helm integration  
- cloud-native artifact registry  
- RAG/AI indexing infrastructure  

Each extension will follow the same deterministic, contract-driven design.
