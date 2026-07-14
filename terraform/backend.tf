terraform {
  backend "s3" {
    bucket = "${var.state_bucket_name}"
    key    = "${var.service_name}/terraform.tfstate"
    region = var.aws_region
  }
}
