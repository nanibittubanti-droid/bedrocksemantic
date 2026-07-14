module "ecr" {
  source = "../ecr"

  repository_name = var.ecr_repository_name
  tags            = var.tags
}

module "iam" {
  source = "../iam"

  role_name         = var.role_name
  policy_name       = var.policy_name
  policy_description = var.policy_description
  policy_json       = var.policy_json
  tags              = var.tags
}

module "networking" {
  source = "../networking"

  vpc_cidr             = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  availability_zones   = var.availability_zones
  tags                 = var.tags
}

module "kms" {
  source = "../kms"

  alias_name = "alias/${var.service_name}"
  description = "KMS key for ${var.service_name}"
  tags       = var.tags
}

module "cloudwatch" {
  source = "../cloudwatch"

  log_group_name = "/aws/${var.service_name}/application"
  tags           = var.tags
}

module "monitoring" {
  source = "../monitoring"

  alarm_name         = "${var.service_name}-high-error-rate"
  metric_name        = "Errors"
  namespace          = "AWS/Logs"
  threshold          = 5
  alarm_description  = "Alarm for ${var.service_name} errors"
  dimensions         = { LogGroupName = module.cloudwatch.log_group_name }
  tags               = var.tags
}

module "secrets" {
  source = "../secrets"

  secret_name = "${var.service_name}/api-key"
  description = "API key for ${var.service_name}"
  secret_string = var.secret_value
  tags         = var.tags
}

module "bedrock_agentcore" {
  source = "../bedrock_agentcore"

  agent_name    = var.service_name
  description   = "Bedrock AgentCore agent for ${var.service_name}"
  foundation_model = "anthropic.claude-3-sonnet-20240229-v1:0"
  instruction   = "You are a helpful assistant for ${var.service_name}."
  tags          = var.tags
}
