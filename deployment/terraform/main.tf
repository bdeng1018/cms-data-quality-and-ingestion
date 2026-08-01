# ==============================================================================
# CMS Data Quality & Ingestion Pipeline (Terraform Provisioning)
# ==============================================================================
# Intent:
#   Provision deterministic infrastructure for running the CMS ingestion pipeline.
#   This Terraform module defines reproducible compute, storage, and networking
#   resources that mirror docker-compose and K8s deployment guarantees.
#
# Determinism Guarantees:
#   - Pinned provider versions.
#   - Stable resource naming.
#   - Reproducible storage + compute configuration.
#
# Side Effects:
#   - Creates cloud compute instance(s).
#   - Creates storage buckets or volumes.
#   - Creates networking resources.
#
# Future Extensions:
#   - Add autoscaling groups.
#   - Add cloud storage ingestion endpoints.
#   - Add distributed ingestion cluster.
# ==============================================================================

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# ==============================================================================
# Compute Instance (Deterministic Runner)
# ==============================================================================
# Intent:
#   Provision a deterministic compute instance for running the CMS ingestion
#   pipeline. Mirrors docker-compose and K8s resource limits.
#
# Determinism:
#   - Instance type pinned.
#   - AMI pinned.
# ==============================================================================
resource "aws_instance" "cms_pipeline" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name       = "cms-pipeline-runner"
    Pipeline   = "CMS-Ingestion"
    Provenance = "terraform"
  }
}

# ==============================================================================
# Storage Bucket (Artifacts + Logs)
# ==============================================================================
# Intent:
#   Provide deterministic cloud storage for pipeline artifacts, logs, manifests,
#   and artifact registries.
#
# Determinism:
#   - Bucket name pinned.
#   - Versioning enabled.
# ==============================================================================
resource "aws_s3_bucket" "cms_artifacts" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  tags = {
    Name       = "cms-artifacts"
    Pipeline   = "CMS-Ingestion"
    Provenance = "terraform"
  }
}

# ==============================================================================
# Networking (Optional)
# ==============================================================================
# Intent:
#   Provide deterministic networking resources for pipeline execution.
#
# Future Extensions:
#   - Add VPC.
#   - Add subnets.
#   - Add security groups.
# ==============================================================================
resource "aws_security_group" "cms_pipeline_sg" {
  name        = "cms-pipeline-sg"
  description = "Security group for CMS ingestion pipeline"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name       = "cms-pipeline-sg"
    Pipeline   = "CMS-Ingestion"
    Provenance = "terraform"
  }
}