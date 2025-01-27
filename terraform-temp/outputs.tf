output "api_gateway_endpoint" {
  value = aws_apigatewayv2_api.main.api_endpoint
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.main.id
}

output "cognito_client_id" {
  value = aws_cognito_user_pool_client.client.id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.storage.id
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.main.name
}
