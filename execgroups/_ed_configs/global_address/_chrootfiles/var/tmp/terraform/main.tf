resource "google_compute_global_address" "global_address_block" {
  project      = "${var.gcloud_project}"
  name       = "${var.global_address_name}"
  purpose      = "VPC_PEERING"
  address_type = "INTERNAL"
  ip_version   = "IPV4"
  prefix_length = "${var.global_address_prefix_length}"
  network       = "${var.vpc_self_link}"
}
