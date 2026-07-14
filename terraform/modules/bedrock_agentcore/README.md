This module provisions the supporting AWS resources for the Bedrock AgentCore runtime deployment path.

It currently targets:
- ECR repository for the container image
- IAM role and policy for runtime execution
- CloudWatch logging
- Secrets Manager and KMS integration

Note: the AWS provider used in this repository does not expose a verified Bedrock AgentCore runtime resource in the installed schema, so this module focuses on the deployable infrastructure layer around the runtime.
