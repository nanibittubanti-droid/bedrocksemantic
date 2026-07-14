variable "aws_region" {
  description = "AWS region for the qa environment."
  type        = string
  default     = "us-east-1"
}

variable "service_name" {
  description = "Service name prefix."
  type        = string
  default     = "waf-assessment-platform-qa"
}

variable "ecr_repository_name" {
  description = "ECR repository name."
  type        = string
  default     = "waf-assessment-agent-repo-qa"
}

variable "artifact_bucket_name" {
  description = "Artifact bucket name."
  type        = string
  default     = "waf-assessment-artifacts-qa"
}

variable "tags" {
  description = "Tags for qa resources."
  type        = map(string)
  default     = {}
}

variable "state_bucket_name" {
  description = "Terraform state bucket name."
  type        = string
  default     = "waf-assessment-terraform-state"
}
