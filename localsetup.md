# Local Setup and End-to-End Testing

This guide describes how to set up and run the Bedrock AgentCore project locally, validate the Python application, build the Docker image, and verify the Terraform infrastructure configuration.

## Prerequisites

- Python 3.12 installed
- Docker installed
- Terraform 1.5+ installed
- AWS CLI installed and configured if you want to test AWS deployment or CloudWatch integration
- Access to an AWS account with permissions for ECR, IAM, CloudWatch, S3, Secrets Manager, KMS, and Bedrock

## Repository preparation

1. Open a terminal in the repository root:

```bash
cd /d d:\COMPANY\BedrockAgent
```

2. Install Python dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. If you want Poetry/pyproject support, install the same dependencies in your environment or use `pip` from `requirements.txt`.

## Environment variables

Set the following variables before running the application locally.

```bash
export AWS_REGION=us-east-1
export MODEL_ID=amazon.titan-text-bison
export DATABASE_URL=postgresql://user:password@localhost:5432/dbname
export LOG_LEVEL=INFO
export LOG_FORMAT=plain
export SERVICE_NAME=waf-assessment-platform
export ENVIRONMENT=local
```

For observability and OpenTelemetry testing, optionally set:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_SERVICE_NAME=waf-assessment-platform-local
export OTEL_ENVIRONMENT=local
```

If you want to run a single assessment without a file, set `ASSESSMENT_PAYLOAD`:

```bash
export ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}'
```

## Run the application locally

1. Run the Python runtime:

```bash
python -m app.main
```

2. If using `ASSESSMENT_PAYLOAD`, the runtime will parse the payload and print the assessment result in JSON format.

3. If you want to pass a JSON request file instead:

```bash
python -m app.main /path/to/request.json
```

## Build and run the Docker image locally

1. Build the Docker image:

```bash
docker build -t waf-assessment-platform -f docker/Dockerfile .
```

2. Run the container locally with environment variables:

```bash
docker run --rm \
  -e AWS_REGION=us-east-1 \
  -e MODEL_ID=amazon.titan-text-bison \
  -e DATABASE_URL=postgresql://user:password@localhost:5432/dbname \
  -e LOG_LEVEL=INFO \
  -e LOG_FORMAT=plain \
  -e SERVICE_NAME=waf-assessment-platform \
  -e ENVIRONMENT=local \
  -e ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}' \
  waf-assessment-platform
```

## Terraform validation

The repository includes `terraform/` for infrastructure configuration.

1. Initialize Terraform locally:

```bash
terraform -chdir=terraform init -backend=false
```

2. Validate the Terraform configuration:

```bash
terraform -chdir=terraform validate
```

3. Generate a plan if you want to inspect the expected changes:

```bash
terraform -chdir=terraform plan -var="aws_region=us-east-1" -var="service_name=waf-assessment-platform-local"
```

> Note: For actual AWS deployment, update `terraform/terraform.tfvars` or pass the real variable values, and configure the S3 backend or AWS credentials.

## End-to-end checks

1. Python imports and runtime should load successfully.
2. The Docker image should build without errors.
3. Terraform should initialize and validate.
4. If AWS credentials are configured, the project can deploy using the existing GitHub Actions workflow or by running Terraform manually.

## GitHub Actions local test guidance

- There is a build workflow at `.github/workflows/build.yml`.
- There is a deploy workflow at `.github/workflows/deploy-dev.yml`.
- Local testing of these workflows can be performed by ensuring the same environment variables and secrets are available.

## Key files

- `app/main.py` — application entrypoint
- `app/config.py` — runtime configuration and environment variable load
- `app/logging_config.py` — logging setup with trace context support
- `app/observability.py` — OpenTelemetry trace and metric setup
- `docker/Dockerfile` — container build
- `terraform/main.tf` — root infrastructure configuration
- `.github/workflows/deploy-dev.yml` — deployment workflow
- `requirements.txt` — Python dependencies

## Troubleshooting

- If the application fails to import, verify `PYTHONPATH` is set to the repository root or run from the repo root.
- If Docker build fails, ensure the Python base image is reachable and dependencies are installed properly.
- If Terraform validation fails, ensure `terraform init` completed successfully and the root module file names are correct.
- For local observability testing, if `OTEL_EXPORTER_OTLP_ENDPOINT` is not configured, the runtime will fall back to console trace and metric export.
