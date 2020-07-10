resource "google_compute_network" "vpc" {
  project       = "${var.gcloud_project}"
  name          = "${var.vpc_name}"
  auto_create_subnetworks = "false"
  routing_mode  = "${var.routing_mode}"
}
