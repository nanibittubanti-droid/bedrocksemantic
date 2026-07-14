resource "aws_cloudwatch_log_group" "this" {
  name              = var.log_group_name
  retention_in_days = var.retention_in_days
  tags              = var.tags
}

resource "aws_cloudwatch_log_metric_filter" "error_count" {
  name           = replace(replace(var.log_group_name, "/", "-"), "_", "-")
  log_group_name = aws_cloudwatch_log_group.this.name
  pattern        = "ERROR"

  metric_transformation {
    name          = var.metric_name
    namespace     = var.metric_namespace
    value         = "1"
    default_value = 0
  }
}
