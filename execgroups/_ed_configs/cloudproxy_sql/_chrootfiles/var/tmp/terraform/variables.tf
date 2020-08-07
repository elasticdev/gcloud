variable "gcloud_region" {
    description = "gcloud_region"
    default = "us-west1"
}

variable "zone" {
    description = "zone"
    default = "us-west1-b"
}

variable "disk_size" {
    description = "disk size in gb"
    default = 10
}

variable "instance_type" {
    description = "instance_type"
    default = "f1-micro"
}

variable "image" {
    description = "image"
    default     = "cos-cloud/cos-stable" 
}

variable "gcloud_project" {
    description = "gcloud_project"
}

variable "vpc_self_link" {
    description = "self_link of the vpc"
}

variable "vpc_name" {
    description = "Name of the vpc network"
}
