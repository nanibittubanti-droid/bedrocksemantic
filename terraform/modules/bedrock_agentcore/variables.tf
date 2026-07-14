variable "agent_name" {
  description = "Name of the Bedrock AgentCore agent."
  type        = string
}

variable "description" {
  description = "Description of the agent."
  type        = string
  default     = "Managed by Terraform"
}

variable "foundation_model" {
  description = "Foundation model identifier."
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0"
}

variable "instruction" {
  description = "Instruction prompt for the agent."
  type        = string
  default     = "You are a helpful AI assistant."
}

variable "tags" {
  description = "Tags to apply."
  type        = map(string)
  default     = {}
}
