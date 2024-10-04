terraform {
  required_version = "~> 1.9.3"

  required_providers {
    google = "4.40.0"
  }

  backend "gcs" {
    bucket = "gcs-terraform-deploy"
    prefix = "iac"
  }

}
