resource "google_service_account" "proxy_account" {
  project       = var.gcloud_project
  account_id    = "cloud-sql-proxy"
}

resource "google_project_iam_member" "role" {
  project       = var.gcloud_project
  role          = "roles/cloudsql.editor"
  member        = "serviceAccount:${google_service_account.proxy_account.email}"
}

resource "google_service_account_key" "key" {
  service_account_id = google_service_account.proxy_account.name
}

data "google_compute_subnetwork" "regional_subnet" {
  project       = var.gcloud_project
  name          = var.vpc_name
  region        = var.gcloud_region
}

resource "google_compute_instance" "default" {
  project         = var.gcloud_project
  name            = "${var.vpc_name}-${var.gcloud_region}-sql-${var.cloudsql_name}-proxy"
  machine_type    = "${var.instance_type}"
  zone            = "${var.gcloud_zone}"
  tags            = ["ssh","http"]
  desired_status  = "RUNNING"
  allow_stopping_for_update = true

  boot_disk {
    auto_delete  = true
    initialize_params {
      image     = "${var.image}"
      size      = "${var.disk_size}"
      type      = "pd-ssd"             
    }
  }

  labels = {
    network = "${var.vpc_name}"
    vpc     = "${var.vpc_name}"
    zone    = "${var.gcloud_zone}"
    type    = "cloud_sql_proxy"
  }

  metadata = {
    enable-oslogin = "TRUE"
  }

  metadata_startup_script = templatefile("${path.module}/run_cloud_sql_proxy.tpl", {
                                         "db_instance_name"    = var.cloudsql_connection_name,
                                         "service_account_key" = base64decode(google_service_account_key.key.private_key),
                                         })

                                         //"service_account_key" = var.service_account_private_key,
                                         // db_instance_name = module.db.connection_name # e.g. my-project:us-central1:my-db
                                         //"service_account_key" = module.serviceaccount.private_key,
                                         //"db_instance_name"    = "db-proxy",

  network_interface {
    network    = var.vpc_name
    subnetwork = data.google_compute_subnetwork.regional_subnet.self_link 
    access_config {}
  }

  scheduling {
    on_host_maintenance = "MIGRATE"
  }

  service_account {
    email = var.service_account_email_address
    scopes = ["cloud-platform"]
  }

  //email = google_service_account.proxy_account.email

}
