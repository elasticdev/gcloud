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

resource "google_service_networking_connection" "private_vpc_connection" {
  provider                = google-beta
  network                 = "${var.vpc_self_link}"
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = ["${var.global_address_name}"]
}
