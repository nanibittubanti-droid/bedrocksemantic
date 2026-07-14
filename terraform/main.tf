terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
    awscc = {
      source  = "hashicorp/awscc"
      version = ">= 1.0.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "awscc" {
  region = var.aws_region
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = var.ecr_repository_name
  tags            = var.tags
}

module "iam" {
  source = "./modules/iam"

  role_name          = "${var.service_name}-agent-execution-role"
  policy_name        = "${var.service_name}-bedrock-agent-policy"
  policy_description = "Permissions required for Bedrock AgentCore runtime and assessment data access."
  assume_role_policy = data.aws_iam_policy_document.agent_assume_role_policy.json
  policy_json        = data.aws_iam_policy_document.agent_permissions_policy.json
  tags               = var.tags
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

  alias_name  = "alias/${var.service_name}"
  description = "KMS key for ${var.service_name}"
  tags        = var.tags
}

module "cloudwatch" {
  source = "./modules/cloudwatch"

  log_group_name   = "/aws/${var.service_name}/application"
  metric_name      = "ApplicationErrorCount"
  metric_namespace = "BedrockAgent"
  tags             = var.tags
}

module "monitoring" {
  source = "./modules/monitoring"

  alarm_name        = "${var.service_name}-application-error-alarm"
  metric_name       = "ApplicationErrorCount"
  namespace         = "BedrockAgent"
  threshold         = 5
  alarm_description = "Alert when the application error metric exceeds threshold"
  tags              = var.tags
}

module "secrets" {
  source = "./modules/secrets"

  secret_name   = "${var.service_name}/api-key"
  description   = "Runtime API secret for ${var.service_name}"
  secret_string = "changeme"
  tags          = var.tags
}

resource "awscc_bedrockagentcore_runtime" "this" {
  count = var.ecr_image_uri != "" ? 1 : 0

  agent_runtime_name = "${var.service_name}-runtime"
  description        = "Bedrock AgentCore runtime for ${var.service_name}"
  role_arn           = module.iam.role_arn
  image_uri          = var.ecr_image_uri
  tags               = var.tags
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

output "monitoring_alarm_arn" {
  description = "CloudWatch alarm ARN for application error monitoring."
  value       = module.monitoring.alarm_arn
}

output "secret_arn" {
  description = "Secrets Manager secret ARN for runtime secrets."
  value       = module.secrets.secret_arn
}

output "agent_runtime_id" {
  description = "The ID of the Bedrock AgentCore runtime."
  value       = try(awscc_bedrockagentcore_runtime.this[0].agent_runtime_id, "")
}

output "agent_runtime_arn" {
  description = "The ARN of the Bedrock AgentCore runtime."
  value       = try(awscc_bedrockagentcore_runtime.this[0].agent_runtime_arn, "")
}
