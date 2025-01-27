terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "pioneer-terraform-state-179079437960"
    key    = "terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = "us-west-2"

  default_tags {
    tags = {
      Project     = "CloudPioneer"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

module "iam" {
  source            = "./modules/iam"
  github_repository = "ashedrack/Pioneer"
}

output "github_actions_role_arn" {
  value = module.iam.github_actions_role_arn
}
