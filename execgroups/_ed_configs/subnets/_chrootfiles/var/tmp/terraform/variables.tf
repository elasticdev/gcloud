variable "project_id" {
    description = "project_id"
    default = "testproject-11111"
}

variable "vpc_name" {
    description = "Name of the vpc network"
    default = "test"
}

variable "public_cidr" {
    description = "public_cidr"
    default = "10.10.10.0/24"
}

variable "private_cidr" {
    description = "private_cidr"
    default = "10.10.20.0/24"
}

variable "default_region" {
    description = "default region"
    default = "us-west1"
}
