terraform {
  backend "s3" {
    bucket = "pioneer-terraform-state"
    key    = "terraform.tfstate"
    region = "us-west-2"
  }
}
