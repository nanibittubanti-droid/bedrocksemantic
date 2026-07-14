This module provisions the supporting AWS resources for the Bedrock AgentCore runtime deployment path.

It currently targets:
- ECR repository for the container image
- IAM role and policy for runtime execution
- CloudWatch logging
- Secrets Manager and KMS integration

## Local testing

To test this module locally, run:

```bash
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

If you want to test a real deployment, configure AWS credentials and run:

```bash
terraform -chdir=terraform init \
  -backend-config="bucket=<your-state-bucket>" \
  -backend-config="key=waf-assessment-platform/terraform.tfstate" \
  -backend-config="region=us-east-1"

terraform -chdir=terraform plan
```

## GitHub Actions testing

The deployment workflow in `.github/workflows/deploy-dev.yml` uses this module indirectly through the Terraform root module.

Required repository secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ACCOUNT_ID`
- `TF_STATE_BUCKET_NAME`

Note: the AWS provider used in this repository does not expose a verified Bedrock AgentCore runtime resource in the installed schema, so this module focuses on the deployable infrastructure layer around the runtime.
