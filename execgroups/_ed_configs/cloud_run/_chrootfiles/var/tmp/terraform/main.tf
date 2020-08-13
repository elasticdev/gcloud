provider "google" {
  project = var.gcloud_project
}

# Deploy image to Cloud Run
resource "google_cloud_run_service" "app" {
  name     = var.app-name
  location = var.gcloud_region
  template {
    spec {
      containers {
        image = "gcr.io/${var.gcloud_project}/${var.app-name}"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Create public access
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# Enable public access on Cloud Run service
resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = var.gcloud_region
  project     = var.gcloud_project
  service     = google_cloud_run_service.app.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
