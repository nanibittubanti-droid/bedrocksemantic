variable "role_name" {
  description = "Name of the IAM role."
  type        = string
}

variable "policy_name" {
  description = "Name of the IAM policy."
  type        = string
}

variable "policy_description" {
  description = "Description of the IAM policy."
  type        = string
  default     = "Managed by Terraform"
}

variable "policy_json" {
  description = "JSON policy document for the IAM policy."
  type        = string
}

variable "tags" {
  description = "Tags to apply to IAM resources."
  type        = map(string)
  default     = {}
}
