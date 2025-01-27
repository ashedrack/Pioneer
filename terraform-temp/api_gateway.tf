resource "aws_apigatewayv2_api" "main" {
  name          = var.api_gateway_name
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]  # In production, restrict to your domain
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["*"]
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.main.id
  name   = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip            = "$context.identity.sourceIp"
      requestTime   = "$context.requestTime"
      httpMethod    = "$context.httpMethod"
      routeKey      = "$context.routeKey"
      status        = "$context.status"
      protocol      = "$context.protocol"
      responseTime  = "$context.responseLatency"
    })
  }
}
