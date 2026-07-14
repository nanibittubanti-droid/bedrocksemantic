variable "aws_region" {
  description = "AWS region for deployment."
  type        = string
  default     = "us-east-1"
}

variable "service_name" {
  description = "Service name for naming resources."
  type        = string
  default     = "waf-assessment-platform"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository to create."
  type        = string
  default     = "waf-assessment-agent-repo"
}

variable "artifact_bucket_name" {
  description = "Name of the S3 bucket used to store assessment artifacts."
  type        = string
  default     = "waf-assessment-artifacts"
}

variable "tags" {
  description = "Tags to apply to all resources."
  type        = map(string)
  default = {
    Project = "WAF Assessment Platform"
    Owner   = "AI Engineering"
    Env     = "prod"
  }
}

variable "state_bucket_name" {
  description = "S3 bucket name for storing Terraform state when using S3 backend."
  type        = string
  default     = "waf-assessment-terraform-state"
}
