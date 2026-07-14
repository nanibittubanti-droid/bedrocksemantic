terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = var.ecr_repository_name
  tags            = var.tags
}

module "iam" {
  source = "./modules/iam"

  role_name         = "${var.service_name}-agent-execution-role"
  policy_name       = "${var.service_name}-bedrock-agent-policy"
  policy_description = "Permissions required for Bedrock AgentCore runtime and assessment data access."
  policy_json       = data.aws_iam_policy_document.agent_permissions_policy.json
  tags              = var.tags
}

module "networking" {
  source = "./modules/networking"

  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24"]
  availability_zones   = ["${var.aws_region}a", "${var.aws_region}b"]
  tags                 = var.tags
}

module "kms" {
  source = "./modules/kms"

  alias_name = "alias/${var.service_name}"
  description = "KMS key for ${var.service_name}"
  tags       = var.tags
}

module "cloudwatch" {
  source = "./modules/cloudwatch"

  log_group_name = "/aws/${var.service_name}/application"
  tags           = var.tags
}

module "secrets" {
  source = "./modules/secrets"

  secret_name = "${var.service_name}/api-key"
  description = "Runtime API secret for ${var.service_name}"
  secret_string = "changeme"
  tags         = var.tags
}

output "ecr_repository_url" {
  description = "ECR repository URL for the Bedrock AgentCore container image."
  value       = module.ecr.repository_url
}

output "agent_execution_role_arn" {
  description = "IAM role ARN for AgentCore runtime execution."
  value       = module.iam.role_arn
}

output "artifact_bucket_name" {
  description = "S3 bucket for uploaded assessment artifacts."
  value       = var.artifact_bucket_name
}

output "kms_key_arn" {
  description = "KMS key ARN used by the runtime stack."
  value       = module.kms.key_arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for runtime logs."
  value       = module.cloudwatch.log_group_name
}

output "secret_arn" {
  description = "Secrets Manager secret ARN for runtime secrets."
  value       = module.secrets.secret_arn
}
