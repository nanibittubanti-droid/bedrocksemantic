terraform {
  required_version = ">= 1.5.0"
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

resource "aws_ecr_repository" "agent_repo" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = var.tags
}

resource "aws_iam_role" "agent_execution" {
  name = "${var.service_name}-agent-execution-role"
  assume_role_policy = data.aws_iam_policy_document.agent_assume_role_policy.json
  tags = var.tags
}

resource "aws_iam_policy" "agent_permissions" {
  name        = "${var.service_name}-bedrock-agent-policy"
  description = "Permissions required for Bedrock AgentCore runtime and assessment data access."
  policy = data.aws_iam_policy_document.agent_permissions_policy.json
  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "agent_policy_attach" {
  role       = aws_iam_role.agent_execution.name
  policy_arn = aws_iam_policy.agent_permissions.arn
}

resource "aws_s3_bucket" "artifact_bucket" {
  bucket = var.artifact_bucket_name
  acl    = "private"
  versioning {
    enabled = true
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
      }
    }
  }
  tags = var.tags
}

resource "aws_kms_key" "agent_key" {
  description             = "KMS key for Bedrock AgentCore artifact encryption"
  deletion_window_in_days = 30
  tags                    = var.tags
}

output "ecr_repository_url" {
  description = "ECR repository URL for the Bedrock AgentCore container image."
  value       = aws_ecr_repository.agent_repo.repository_url
}

output "agent_execution_role_arn" {
  description = "IAM role ARN for AgentCore runtime execution."
  value       = aws_iam_role.agent_execution.arn
}

output "artifact_bucket_name" {
  description = "S3 bucket for uploaded assessment artifacts."
  value       = aws_s3_bucket.artifact_bucket.id
}
