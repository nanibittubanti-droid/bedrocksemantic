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

module "app" {
  source = "../../"

  aws_region            = var.aws_region
  service_name          = var.service_name
  ecr_repository_name   = var.ecr_repository_name
  artifact_bucket_name  = var.artifact_bucket_name
  tags                  = merge(var.tags, { Environment = "qa" })
  state_bucket_name     = var.state_bucket_name
}
