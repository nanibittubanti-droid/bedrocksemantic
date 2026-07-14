resource "aws_bedrockagentcore_agent" "this" {
  agent_name = var.agent_name
  description = var.description
  foundation_model = var.foundation_model
  instruction = var.instruction

  tags = var.tags
}
