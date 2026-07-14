variable "alarm_name" {
  description = "Name of the CloudWatch alarm."
  type        = string
}

variable "comparison_operator" {
  description = "Comparison operator for the alarm."
  type        = string
  default     = "GreaterThanThreshold"
}

variable "evaluation_periods" {
  description = "Number of periods over which data is evaluated."
  type        = number
  default     = 1
}

variable "metric_name" {
  description = "Name of the metric."
  type        = string
}

variable "namespace" {
  description = "Namespace for the metric."
  type        = string
}

variable "period" {
  description = "Evaluation period in seconds."
  type        = number
  default     = 300
}

variable "statistic" {
  description = "Statistic to use."
  type        = string
  default     = "Average"
}

variable "threshold" {
  description = "Threshold for the alarm."
  type        = number
}

variable "alarm_description" {
  description = "Description of the alarm."
  type        = string
  default     = "Managed by Terraform"
}

variable "treat_missing_data" {
  description = "How to handle missing data."
  type        = string
  default     = "notBreaching"
}

variable "dimensions" {
  description = "Metric dimensions."
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags to apply."
  type        = map(string)
  default     = {}
}
