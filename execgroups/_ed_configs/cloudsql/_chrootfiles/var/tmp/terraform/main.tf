resource "google_sql_database" "main" {
  project  = var.gcloud_project
  name     = "main"
  instance = google_sql_database_instance.main_primary.name
}

resource "google_sql_database_instance" "main_primary" {
  region                       = var.gcloud_region
  project                      = var.gcloud_project
  name                         = var.cloudsql_name
  database_version             = var.database_version

  settings {
    tier              = var.database_tier
    availability_type = var.availability_type
    disk_size         = var.disk_size
    ip_configuration {
      ipv4_enabled    = var.ipv4_enabled
      private_network = var.vpc_self_link
    }
  }
}

resource "google_sql_user" "db_user" {
  project  = var.gcloud_project
  name     = var.db_root_user
  instance = google_sql_database_instance.main_primary.name
  password = var.db_root_password
}

