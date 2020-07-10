resource "google_compute_subnetwork" "public_subnet" {
  project       = "${var.gcloud_project}"
  name          = "${var.vpc_name}-${var.gcloud_region}-pub-net"
  ip_cidr_range = "${var.public_cidr}"
  network       = "${var.vpc_name}"
  region        = "${var.gcloud_region}"
}

resource "google_compute_subnetwork" "private_subnet" {
  project       = "${var.gcloud_project}"
  name          = "${var.vpc_name}-${var.gcloud_region}-prv-net"
  ip_cidr_range = "${var.private_cidr}"
  network       = "${var.vpc_name}"
  region        = "${var.gcloud_region}"
}
