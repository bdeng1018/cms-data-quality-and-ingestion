# ==============================================================================
# CMS Data Quality & Ingestion Pipeline (Terraform Outputs)
# ==============================================================================
# Intent:
#   Expose deterministic infrastructure outputs for downstream tooling, CI/CD,
#   pipeline runners, and provenance tracking. These outputs allow the pipeline
#   to reference provisioned compute, storage, and networking resources.
#
# Determinism Guarantees:
#   - Stable output names.
#   - Stable resource references.
#   - Outputs map directly to manifest.provenance fields.
#
# Future Extensions:
#   - Add distributed ingestion cluster outputs.
#   - Add cloud storage ingestion endpoints.
#   - Add autoscaling metadata.
# ==============================================================================

output "cms_pipeline_instance_id" {
  description = "EC2 instance ID for deterministic pipeline execution"
  value       = aws_instance.cms_pipeline.id
}

output "cms_pipeline_public_ip" {
  description = "Public IP for pipeline runner (optional)"
  value       = aws_instance.cms_pipeline.public_ip
}

output "cms_artifacts_bucket" {
  description = "S3 bucket for pipeline artifacts + logs"
  value       = aws_s3_bucket.cms_artifacts.bucket
}

output "cms_pipeline_security_group" {
  description = "Security group for CMS ingestion pipeline"
  value       = aws_security_group.cms_pipeline_sg.id
}