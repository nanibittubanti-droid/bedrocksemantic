variable "log_group_name" {
  description = "Name of the CloudWatch log group."
  type        = string
}

variable "metric_name" {
  description = "Name of the application metric created from log events."
  type        = string
  default     = "ApplicationErrorCount"
}

variable "metric_namespace" {
  description = "CloudWatch namespace for application metrics."
  type        = string
  default     = "BedrockAgent"
}

variable "retention_in_days" {
  description = "Number of days to retain logs."
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply."
  type        = map(string)
  default     = {}
}
