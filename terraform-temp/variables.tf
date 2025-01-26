variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "cloud-pioneer"
}

variable "cognito_user_pool_name" {
  description = "Cognito User Pool name"
  type        = string
  default     = "cloud-pioneer-users"
}

variable "api_gateway_name" {
  description = "API Gateway name"
  type        = string
  default     = "cloud-pioneer-api"
}
