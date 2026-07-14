output "ecr_repository_url" {
  description = "ECR repository URL."
  value       = module.ecr.repository_url
}

output "iam_role_arn" {
  description = "IAM role ARN."
  value       = module.iam.role_arn
}

output "vpc_id" {
  description = "VPC ID."
  value       = module.networking.vpc_id
}

output "kms_key_arn" {
  description = "KMS key ARN."
  value       = module.kms.key_arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name."
  value       = module.cloudwatch.log_group_name
}

output "monitoring_alarm_arn" {
  description = "CloudWatch alarm ARN."
  value       = module.monitoring.alarm_arn
}

output "secret_arn" {
  description = "Secrets Manager secret ARN."
  value       = module.secrets.secret_arn
}

