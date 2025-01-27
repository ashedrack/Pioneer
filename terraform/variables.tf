variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "pioneer"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}
