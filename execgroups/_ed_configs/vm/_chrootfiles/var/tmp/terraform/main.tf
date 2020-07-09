resource "google_compute_instance" "default" {
  project       = "${var.project_id}"
  name          = "${var.vpc_name}-${var.default_region}-instance1"
  machine_type  = "${var.instance_type}"
  zone          = "${var.zone}"
  tags          = ["ssh","http"]

  boot_disk {
    auto_delete  = true
    initialize_params {
      image     = "${var.image}"
      size      = "${var.disk_size}"
    }
  }

  labels = {
    network = "${var.vpc_name}"
    vpc     = "${var.vpc_name}"
    zone    = "${var.zone}"
  }

  //metadata = {
  //        startup-script = <<SCRIPT
  //        apt-get -y update
  //        apt-get -y install nginx
  //        export HOSTNAME=$(hostname | tr -d '\n')
  //        export PRIVATE_IP=$(curl -sf -H 'Metadata-Flavor:Google' http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip | tr -d '\n')
  //        echo "Welcome to $HOSTNAME - $PRIVATE_IP" > /usr/share/nginx/www/index.html
  //        service nginx start
  //        SCRIPT
  //} 

  network_interface {
      network = "${var.vpc_name}"
      subnetwork = "https://www.googleapis.com/compute/v1/projects/${var.project_id}/regions/${var.default_region}/subnetworks/${var.vpc_name}-${var.default_region}-pub-net"
      access_config {
        // Ephemeral IP
      }
  }

}

// resource "google_compute_instance_template" "tpl" {
//   project         = "${var.project_id}"
//   name            = "${var.vpc_name}-template"
//   machine_type    = "${var.instance_type}"
//   tags          = ["ssh","http"]
// 
//   disk {
//     source_image = "${var.image}"
//     disk_size_gb = "${var.disk_size}"
//     auto_delete  = true
//     boot         = true
//   }
// 
//   network_interface {
//       network = "${var.vpc_name}"
//       subnetwork = "https://www.googleapis.com/compute/v1/projects/${var.project_id}/regions/${var.default_region}/subnetworks/${var.vpc_name}-${var.default_region}-pub-net"
//       access_config {
//         // Ephemeral IP
//       }
//   }
// 
//   metadata = {
//       enable-oslogin = "TRUE"
//     }
// }
// 
// resource "google_compute_instance_from_template" "tpl" {
//   project    = "${var.project_id}"
//   name       = "${var.vpc_name}-${var.zone}-${var.hostname_suffix}"
//   zone       = "${var.zone}"
// 
//   source_instance_template = google_compute_instance_template.tpl.id
// 
//   can_ip_forward = false
// 
//   labels = {
//     hostname = "${var.vpc_name}-${var.zone}-${var.hostname_suffix}"
//     name     = "${var.vpc_name}-${var.zone}-${var.hostname_suffix}"
//     zone     = "${var.zone}"
//   }
// 
// }
