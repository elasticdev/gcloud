variable "gcloud_project" {
    description = "gcloud_project"
    default = "test-project"
}

variable "gcloud_region" {
    description = "gcloud_region"
    default = "us-west1"
}

variable "app-name" {
    description = "name of the cloud run app"
    default = "flask-webapp"
}
