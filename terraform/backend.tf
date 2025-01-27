terraform {
  backend "s3" {
    bucket = "pioneer-terraform-state-1gb"
    key    = "terraform.tfstate"
    region = "us-west-2"
  }
}
