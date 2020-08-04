resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = "${var.vpc_self_link}"
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = ["${var.global_address_name}"]
}
