install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

lint:
	python -m py_compile app/*.py app/**/*.py tests/**/*.py
	python -m ruff check app tests

test:
	python -m pytest tests

docker-build:
	docker build -t waf-assessment-platform -f docker/Dockerfile .

docker-run:
	docker run --rm \
		-e AWS_REGION=${AWS_REGION:-us-east-1} \
		-e MODEL_ID=${MODEL_ID:-amazon.titan-text-bison} \
		-e ASSESSMENT_PAYLOAD='{"request_id":"req-001","artifacts":[{"artifact_type":"terraform","name":"example","content":"resource \"aws_s3_bucket\" \"example\" {}"}]}' \
		waf-assessment-platform

terraform-init:
	terraform -chdir=terraform init \
		-backend-config="bucket=${TF_STATE_BUCKET_NAME:-waf-assessment-terraform-state}" \
		-backend-config="key=${TF_STATE_KEY:-waf-assessment-platform/terraform.tfstate}" \
		-backend-config="region=${AWS_REGION:-us-east-1}"

terraform-plan:
	terraform -chdir=terraform plan

terraform-apply:
	terraform -chdir=terraform apply -auto-approve

terraform-destroy:
	terraform -chdir=terraform destroy -auto-approve

deploy: install lint test docker-build terraform-init terraform-plan terraform-apply
