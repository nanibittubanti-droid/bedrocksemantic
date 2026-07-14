variable "description" {
  description = "Description of the KMS key."
  type        = string
  default     = "Managed by Terraform"
}

variable "alias_name" {
  description = "Alias for the KMS key."
  type        = string
}

variable "deletion_window_in_days" {
  description = "Deletion window for the KMS key."
  type        = number
  default     = 30
}

variable "enable_key_rotation" {
  description = "Enable automatic key rotation."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply."
  type        = map(string)
  default     = {}
}
