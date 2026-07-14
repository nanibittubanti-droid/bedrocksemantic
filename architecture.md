# Architecture Overview

This repository implements an end-to-end AWS Bedrock AgentCore runtime deployment for a Python AI agent packaged as a Docker container and deployed through Terraform.

## High-level architecture

1. **Application layer**
   - `app/` contains the Python runtime entrypoint, agent orchestration, prompts, plugins, services, and models.
   - The runtime is executed by `python -m app.main` inside a container.

2. **Container layer**
   - `docker/Dockerfile` builds a minimal Python 3.12 container image.
   - The image installs dependencies from `requirements.txt`, copies the application source, and sets the entrypoint.
   - The GitHub Actions workflow builds and pushes this image to AWS ECR.

3. **Infrastructure layer**
   - `terraform/` contains the IaC definition for deployment.
   - The root Terraform module provisions:
     - `awscc` provider for Bedrock AgentCore runtime resources
     - `aws` provider for supporting AWS resources
     - ECR repository module
     - IAM role and policy module
     - VPC and subnet networking module
     - KMS key module
     - CloudWatch log group module
     - Secrets Manager module
     - Bedrock AgentCore runtime resource

4. **Deployment workflow**
   - `.github/workflows/deploy-dev.yml` builds and pushes the Docker image to ECR and then runs Terraform apply.
   - The workflow passes the built image URI into Terraform via `ecr_image_uri`.

## Detailed architecture

### Runtime container and ECR

- `docker/Dockerfile` produces the container image.
- The deployment workflow builds the image using the repository name `ECR_REPOSITORY` and tags it as `latest`.
- The built image is pushed to the AWS ECR repository.
- Terraform receives the full ECR image URI and supplies it to the Bedrock runtime resource.

### Terraform root module

- `terraform/main.tf` now includes both:
  - `aws` provider for AWS resources such as IAM, VPC, CloudWatch, Secrets Manager.
  - `awscc` provider for Bedrock AgentCore runtime support.
- The root module composes separate infrastructure modules:
  - `terraform/modules/ecr`
  - `terraform/modules/iam`
  - `terraform/modules/networking`
  - `terraform/modules/kms`
  - `terraform/modules/cloudwatch`
  - `terraform/modules/secrets`
- `awscc_bedrockagentcore_runtime.this` is created only when `var.ecr_image_uri` is set.
- The Bedrock runtime resource is configured with:
  - `agent_runtime_name`
  - `description`
  - `role_arn`
  - `image_uri`
  - `tags`

### IAM and Bedrock execution

- The IAM module now accepts a custom assume role policy document.
- `terraform/data.tf` defines the Bedrock assume-role policy for `bedrock-agentcore.amazonaws.com`.
- The runtime permission policy includes ECR permissions required to pull the container image:
  - `ecr:GetAuthorizationToken`
  - `ecr:BatchGetImage`
  - `ecr:GetDownloadUrlForLayer`
  - `ecr:BatchCheckLayerAvailability`
- It also includes Bedrock model invocation and common runtime permissions.

### Networking and security

- The `networking` module creates a VPC, public subnets, private subnets, an internet gateway, and routing for public traffic.
- The `secrets` module stores a runtime API secret in AWS Secrets Manager.
- The `cloudwatch` module provisions a log group for runtime logging, a metric filter for application errors, and a CloudWatch metric namespace for observability.
- The `kms` module provisions a KMS key for encryption support.

## CI/CD flow

1. GitHub Actions workflow checks out the repo.
2. AWS credentials are configured using secrets.
3. Terraform is installed.
4. Docker image is built from `docker/Dockerfile` and pushed to the ECR repository.
5. Terraform is initialized using the S3 backend when available, otherwise local init is used.
6. Terraform apply runs with the image URI passed as:
   - `-var="ecr_image_uri=${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest"`
7. The Bedrock runtime is created and linked to the ECR image.

## Key file references

- `app/` — Python application source
- `docker/Dockerfile` — runtime container build
- `terraform/main.tf` — root Terraform orchestration
- `terraform/variables.tf` — root variable definitions including `ecr_image_uri`
- `terraform/data.tf` — Bedrock assume role and permission policy documents
- `terraform/modules/ecr` — ECR repository
- `terraform/modules/iam` — IAM role and policy
- `terraform/modules/networking` — VPC and subnet infrastructure
- `terraform/modules/kms` — KMS key
- `terraform/modules/cloudwatch` — logging
- `terraform/modules/secrets` — Secrets Manager secret
- `.github/workflows/deploy-dev.yml` — CI/CD deployment workflow

## Design summary

- The project delivers a containerized Python AI agent runtime to AWS Bedrock AgentCore using infrastructure-as-code.
- The build pipeline produces an ECR-hosted image and the Terraform stack creates the Bedrock runtime that consumes that image.
- The architecture is built for repeatable, environment-specific deployment via GitHub Actions and Terraform.
- The design keeps the Bedrock runtime configuration separate from the application code and relies on AWS service roles, ECR, and secure secret storage.

## Post-action workflow summary

After the deployment workflow runs, verify the following:
- The Docker image was built successfully and pushed to the ECR repository.
- Terraform initialized correctly using the configured backend or local fallback.
- Terraform applied the root stack without errors.
- The `awscc_bedrockagentcore_runtime` resource was created and the runtime ARN/ID are available in Terraform outputs.
- CloudWatch log group exists for runtime logs and the Bedrock runtime starts cleanly.

This summary is intended to guide verification after the build and deployment workflow completes successfully.
