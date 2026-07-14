output "ecr_repository_url" {
  description = "ECR repository URL for the Bedrock AgentCore container image."
  value       = aws_ecr_repository.agent_repo.repository_url
}

output "agent_execution_role_arn" {
  description = "IAM role ARN for Bedrock AgentCore runtime execution."
  value       = aws_iam_role.agent_execution.arn
}

output "artifact_bucket_name" {
  description = "S3 bucket name for assessment artifacts."
  value       = aws_s3_bucket.artifact_bucket.id
}
