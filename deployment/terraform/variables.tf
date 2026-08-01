# ==============================================================================
# CMS Data Quality & Ingestion Pipeline (Terraform Variables)
# ==============================================================================
# Intent:
#   Define deterministic, environment-specific variables for Terraform provisioning.
#   These variables control compute, storage, networking, and region selection.
#
# Determinism Guarantees:
#   - Pinned AMI.
#   - Pinned instance type.
#   - Stable bucket naming.
#
# Future Extensions:
#   - Add distributed ingestion cluster variables.
#   - Add cloud storage ingestion endpoints.
#   - Add autoscaling parameters.
# ==============================================================================

variable "region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-west-2"
}

variable "ami_id" {
  description = "Pinned AMI for deterministic pipeline execution"
  type        = string
}

variable "instance_type" {
  description = "Pinned instance type for reproducible performance"
  type        = string
  default     = "t3.large"
}

variable "bucket_name" {
  description = "S3 bucket for pipeline artifacts + logs"
  type        = string
}