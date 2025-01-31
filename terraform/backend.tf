terraform {
  backend "s3" {
    bucket         = "pioneer-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"  # ✅ Make sure this is set correctly
    encrypt        = true
  }
}

