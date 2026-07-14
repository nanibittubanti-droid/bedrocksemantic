variable "secret_name" {
  description = "Name of the Secrets Manager secret."
  type        = string
}

variable "description" {
  description = "Description of the secret."
  type        = string
  default     = "Managed by Terraform"
}

variable "secret_string" {
  description = "Value to store in the secret."
  type        = string
  sensitive   = true
}

variable "recovery_window_in_days" {
  description = "Recovery window for the secret."
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply."
  type        = map(string)
  default     = {}
}
