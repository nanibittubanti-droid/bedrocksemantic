variable "aws_region" {
  description = "AWS region for the dev environment."
  type        = string
  default     = "us-east-1"
}

variable "service_name" {
  description = "Service name prefix."
  type        = string
  default     = "waf-assessment-platform-dev"
}

variable "ecr_repository_name" {
  description = "ECR repository name."
  type        = string
  default     = "waf-assessment-agent-repo-dev"
}

variable "artifact_bucket_name" {
  description = "Artifact bucket name."
  type        = string
  default     = "waf-assessment-artifacts-dev"
}

variable "tags" {
  description = "Tags for dev resources."
  type        = map(string)
  default     = {}
}

variable "state_bucket_name" {
  description = "Terraform state bucket name."
  type        = string
  default     = "waf-assessment-terraform-state"
}
