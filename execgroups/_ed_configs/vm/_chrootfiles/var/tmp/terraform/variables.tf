variable "gcloud_project" {
    description = "gcloud_project"
    default = "testproject-11111"
}

variable "vpc_name" {
    description = "Name of the vpc network"
    default = "test"
}

variable "gcloud_zone" {
    description = "gcloud_zone"
    default = "us-west1-b"
}

variable "gcloud_region" {
    description = "google default region"
    default = "us-west1"
}

variable "disk_size" {
    description = "disk size in gb"
    default = 100
}

variable "hostname_suffix" {
    description = "hostname_suffix"
    default = "test"
}

variable "instance_type" {
    description = "instance_type"
    default = "f1-micro"
}

variable "image" {
    description = "image"
    default = "debian-cloud/debian-9"
}
