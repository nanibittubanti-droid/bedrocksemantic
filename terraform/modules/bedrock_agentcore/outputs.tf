output "agent_id" {
  description = "The ID of the Bedrock AgentCore agent."
  value       = aws_bedrockagentcore_agent.this.id
}
