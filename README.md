# Bedrock Agent

A production-ready enterprise project for deploying a Python AI agent to AWS Bedrock AgentCore Runtime.

## Architecture

- `app/` contains the Python application layers for runtime entrypoint, Semantic Kernel orchestration, agent logic, services, plugins, prompts, and data models.
- `docker/` contains the production Dockerfile for building a minimal Python 3.12 container.
- `terraform/` contains infrastructure-as-code for ECR, IAM, KMS, CloudWatch, networking, and the Bedrock AgentCore Runtime.
- `scripts/` contains helper scripts for build, deploy, and teardown operations.
- `.github/workflows/` contains CI/CD workflows for unit tests, build, Terraform plan, and environment deployments.

## Prerequisites

- AWS account with Bedrock AgentCore permissions
- AWS credentials configured locally or via GitHub secrets/OIDC
- Docker installed for local build and image validation
- Python 3.12 installed for local development
- Terraform installed for infrastructure deployment

## AWS CLI Setup

1. Install and configure AWS CLI:

   ```bash
   aws configure
   ```

2. Ensure the following environment variables are set if you use GitHub Actions secrets:

   - `AWS_REGION`
   - `AWS_ACCOUNT_ID`
   - `AWS_ROLE_TO_ASSUME` (optional, for OIDC or role-based deployment)
   - `ECR_REPOSITORY_NAME`
   - `APP_NAME`
   - `MODEL_ID`

 
   Local testing with Docker Desktop
   ---------------------------------

   If you have Docker Desktop installed, you can run the container locally and connect it to a PostgreSQL instance (e.g., a local Postgres container).

   1. Start a local PostgreSQL container (example using Docker):

   ```bash
   docker run --name waf-postgres -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=app -e POSTGRES_DB=bedrock -p 5432:5432 -d postgres:15
   ```

   2. Build the application image:

   ```bash
   docker build -t waf-assessment-platform -f docker/Dockerfile .
   ```

   3. Run the container and pass required environment variables (replace values as needed):

   ```bash
   docker run --rm \
      -e AWS_REGION=us-east-1 \
      -e MODEL_ID=amazon.titan-text-bison \
      -e DATABASE_URL=postgresql://app:pass@host.docker.internal:5432/bedrock \
      -e ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}' \
      waf-assessment-platform
   ```

   Notes:
   - Use `host.docker.internal` to reach your host Postgres from Docker on Windows/macOS.
   - The container requires `DATABASE_URL` to enable PostgreSQL-backed RAG, session and memory persistence.
   - To ingest `waf.pdf` into the knowledge base, copy it into the image or mount it and run a small script that uses the `PDFIngestService` (a helper script can be added under `scripts/`).
    - To ingest `waf.pdf` into the knowledge base, copy it into the image or mount it and run a small script that uses the `PDFIngestService` (a helper script can be added under `scripts/`).

   Docker Compose ingestion (local):

   1. Place `waf.pdf` under `./data/waf.pdf`.

   2. Start the Postgres DB and run the ingestion service which will import the PDF into the knowledge base:

   ```bash
   docker compose -f docker/docker-compose.yml up --build --abort-on-container-exit ingest
   ```

   3. After ingestion completes, the `ingest` service will exit; keep the DB running if you want to run the agent container separately:

   ```bash
   docker compose -f docker/docker-compose.yml up -d db
   docker compose -f docker/docker-compose.yml run --rm app
   ```
## Docker Setup

Build the container locally:

```bash
docker build -t waf-assessment-platform -f docker/Dockerfile .
```

Run the container locally:

```bash
docker run --rm -e AWS_REGION=us-east-1 -e MODEL_ID=amazon.titan-text-bison -e ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}' waf-assessment-platform
```

## Terraform Setup

1. Copy the example variable file:

   ```bash
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   ```

2. Update values in `terraform/terraform.tfvars`.

3. Initialize Terraform:

   ```bash
   terraform -chdir=terraform init
   ```

4. Validate the configuration:

   ```bash
   terraform -chdir=terraform validate
   ```

## Local Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application locally with a JSON request file:

```bash
python -m app.main ./examples/assessment_request.json
```

## Docker Execution

Build and run locally:

```bash
docker build -t waf-assessment-platform -f docker/Dockerfile .
docker run --rm -e AWS_REGION=us-east-1 -e MODEL_ID=amazon.titan-text-bison -e ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}' waf-assessment-platform
```

The container prints the assessment result to stdout in JSON format.

## Deploy to AWS

1. Build and push the Docker image to ECR.
2. Update Terraform variables to point at the ECR repository and Bedrock model.
3. Apply Terraform:

```bash
terraform -chdir=terraform apply
```

## Destroy Infrastructure

```bash
terraform -chdir=terraform destroy
```

## Troubleshooting

- `Invalid configuration` means environment variables are missing or malformed.
- `Bedrock API request failed` means AWS credentials or Bedrock permissions are not configured correctly.
- Check CloudWatch Logs for runtime errors from AgentCore.
- If Docker build fails, confirm the Python base image is reachable and the `requirements.txt` file is correct.

CI secrets and integration tests
--------------------------------

If you add integration tests that require AWS credentials (Bedrock) or a running Postgres instance, configure secrets in GitHub Actions or your CI provider. Example secrets to set in repository settings:

- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` — for AWS Bedrock API access (use least-privilege credentials).
- `AWS_REGION` — region to use for Bedrock and other AWS services.
- `DATABASE_URL` — connection string for Postgres when running integration tests that require DB access. For CI, prefer a dedicated test DB or run Postgres via services in the workflow.

When running integrations in CI, ensure the workflow creates transient infrastructure (containers) and tears them down after tests. Don't store production credentials in CI; use short-lived credentials or role-based access where possible.
