resource "google_compute_firewall" "internal" {

  project = "${var.gcloud_project}"
  name    = "${var.vpc_name}-fw-internal"
  network = "${var.vpc_name}"

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  source_ranges = [
    "${var.public_cidr}",
    "${var.private_cidr}"
  ]

}

resource "google_compute_firewall" "http" {
  project = "${var.gcloud_project}"
  name    = "${var.vpc_name}-fw-http"
  network = "${var.vpc_name}"

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  target_tags = ["http"] 
}

resource "google_compute_firewall" "bastion" {
  project = "${var.gcloud_project}"
  name    = "${var.vpc_name}-fw-bastion"
  network = "${var.vpc_name}"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  target_tags = ["ssh"]
}

