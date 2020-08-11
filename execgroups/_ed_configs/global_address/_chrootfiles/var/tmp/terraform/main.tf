terraform {
  //required_version = "~> 0.12.24"
  required_providers {
    tfe         = "~> 0.16.0"
    google      = "~> 3.17.0"
    google-beta = "~> 3.17.0" 
  }
}

provider "google-beta" {
  region = var.gcloud_region
  zone   = var.gcloud_zone
}

resource "google_compute_global_address" "global_address_block" {
  provider      = google-beta
  project       = "${var.gcloud_project}"
  name          = "${var.global_address_name}"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  ip_version    = "IPV4"
  prefix_length = "${var.global_address_prefix_length}"
  network       = "${var.vpc_self_link}"
}
