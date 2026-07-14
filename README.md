# Bedrock Agent

A production-ready enterprise project for deploying a Python AI agent to AWS Bedrock AgentCore Runtime.

## Architecture

- `app/` contains the Python application layers for the runtime entrypoint, Semantic Kernel orchestration, agent logic, services, plugins, prompts, and data models.
- `docker/` contains the production Dockerfile for building a minimal Python 3.12 container.
- `terraform/` contains infrastructure-as-code for ECR, IAM, KMS, CloudWatch, networking, secrets, and the supporting runtime stack.
- `scripts/` contains helper scripts for build, deploy, and teardown operations.
- `.github/workflows/` contains CI/CD workflows for unit tests, build, Terraform plan, and environment deployments.

## Prerequisites

Before testing locally or in GitHub Actions, make sure you have:

- An AWS account with access to Bedrock, ECR, IAM, CloudWatch, Secrets Manager, and S3
- AWS credentials configured locally or via GitHub secrets
- Docker installed
- Python 3.12 installed
- Terraform 1.5+ installed

## Local testing

### 1. Configure AWS locally

If you have the AWS CLI installed, run:

```bash
aws configure
```

Set the following environment variables if needed:

```bash
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=<your-account-id>
export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_ACCESS_KEY=<your-secret-key>
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Python application locally

```bash
python -m app.main
```

If you want to pass a sample payload, set:

```bash
export ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}'
```

### 4. Build and test the Docker image locally

```bash
docker build -t waf-assessment-platform -f docker/Dockerfile .
docker run --rm \
  -e AWS_REGION=us-east-1 \
  -e MODEL_ID=amazon.titan-text-bison \
  -e ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}' \
  waf-assessment-platform
```

### 5. Validate Terraform locally

```bash
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

If you want a plan against a real S3 backend, you will need backend access and credentials:

```bash
terraform -chdir=terraform init \
  -backend-config="bucket=<your-state-bucket>" \
  -backend-config="key=waf-assessment-platform/terraform.tfstate" \
  -backend-config="region=us-east-1"

terraform -chdir=terraform plan
```

If you are only validating locally or want the workflow to be less strict, you can use local initialization instead:

```bash
terraform -chdir=terraform init -backend=false
```

## GitHub Actions workflow testing

The repository includes a deployment workflow at `.github/workflows/deploy-dev.yml`.

### Required GitHub secrets

Add these repository secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ACCOUNT_ID`
- `TF_STATE_BUCKET_NAME`

Optional secrets:

- `AWS_REGION`
- `AWS_ROLE_TO_ASSUME` if you use OIDC-based role assumption

### What the workflow does

The workflow will:

1. Configure AWS credentials
2. Build and push the Docker image to ECR
3. Initialize Terraform with the S3 backend when backend settings are available
4. Fall back to local initialization when backend credentials are missing
5. Apply the Terraform stack for the dev environment

### Suggested GitHub Actions environment values

Set these in the workflow or repository variables:

- `AWS_REGION=us-east-1`
- `ECR_REPOSITORY=waf-assessment-agent-repo-dev`
- `TF_STATE_BUCKET_NAME=<your-state-bucket>`

## Terraform setup

1. Copy the example variable file:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

2. Update the values in `terraform/terraform.tfvars`.

3. Initialize Terraform:

```bash
terraform -chdir=terraform init -backend=false
```

4. Validate the configuration:

```bash
terraform -chdir=terraform validate
```

## Deploy to AWS

1. Build and push the Docker image to ECR.
2. Ensure your AWS credentials can access the target account and state bucket.
3. Apply Terraform:

```bash
terraform -chdir=terraform apply -auto-approve
```

## Destroy infrastructure

```bash
terraform -chdir=terraform destroy -auto-approve
```

## Observability

This application is instrumented with OpenTelemetry for traces and metrics. The runtime exports telemetry to the OTLP endpoint configured by `OTEL_EXPORTER_OTLP_ENDPOINT`.

Environment variables supported for observability:

- `OTEL_EXPORTER_OTLP_ENDPOINT` — OTLP collector endpoint for traces and metrics
- `OTEL_SERVICE_NAME` — service name used in trace and metric resource attributes
- `OTEL_ENVIRONMENT` — deployment environment used in trace metadata
- `LOG_FORMAT` — `plain` or `json` output for structured logs

When `OTEL_EXPORTER_OTLP_ENDPOINT` is not configured, the runtime uses console span and metric exporters for local testing.

## Troubleshooting

- `Invalid configuration` means environment variables are missing or malformed.
- `Bedrock API request failed` means AWS credentials or Bedrock permissions are not configured correctly.
- `terraform init` fails because of missing backend credentials; verify your AWS credentials and S3 backend bucket settings.
- Check CloudWatch Logs for runtime errors from the deployed stack.
- If Docker build fails, confirm the Python base image is reachable and the `requirements.txt` file is correct.

## CI secrets and integration tests

If you add integration tests that require AWS access or a running Postgres instance, configure the relevant secrets in GitHub Actions.

Recommended secrets:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ACCOUNT_ID`
- `TF_STATE_BUCKET_NAME`
- `DATABASE_URL` for integration tests that need a database

Use least-privilege credentials and prefer short-lived credentials or role-based access where possible.