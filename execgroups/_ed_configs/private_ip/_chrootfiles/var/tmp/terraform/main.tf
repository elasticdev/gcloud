resource "google_compute_global_address" "private_ip_block" {
  project      = "${var.gcloud_project}"
  name         = "private-ip-block"
  purpose      = "VPC_PEERING"
  address_type = "INTERNAL"
  ip_version   = "IPV4"
  prefix_length = "${var.private_ip_prefix_length}"
  network       = "${var.vpc_self_link}"
}

resource "google_service_networking_connection" "private_vpc_connection" {
  project                 = "${var.gcloud_project}"
  network                 = "${var.vpc_self_link}"
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_block.name]
}
