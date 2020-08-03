resource "google_compute_network" "vpc" {
  project       = "${var.gcloud_project}"
  name          = "${var.vpc_name}"
  auto_create_subnetworks = "${var.auto_create_subnetworks}"
  routing_mode  = "${var.routing_mode}"
}
