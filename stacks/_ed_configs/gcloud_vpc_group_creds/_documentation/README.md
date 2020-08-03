**Description**

  - This stack creates a simple VPC on gcp where the credentials are provided through a user provided execution group

**Required**

| argument      | description                            | var type | default      |
| ------------- | -------------------------------------- | -------- | ------------ |
| vpc_name   | name of the vpc                 | string   | None         |
| gcloud_project      | the project id in gclouod from      | string   | None         |
| google_application_credentials      | the location for the json file gcp      | string     | /tmp/.credentials.json         |
| credential_group      | the name of the private group that contains the credentials json | string   | <nickname>:::gcloud_creds::<project_name> |

**Optional**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| gcloud_region        | google region to create the subnets          | string    | us-west1       |
| routing_mode      | routing mode for vpc    | string   | global         |
| docker_exec_env      | docker container to execute terraform templates    | string   | elasticdev/terraform-run-env         |
| public_cidr      | cidr for public subnet    | string   | 10.10.10.0/24         |
| private_cidr      | cidr for private subnet    | string   | 10.10.20.0/24         |

**Sample entry:**

```
infrastructure:
  vpc:
    stack_name: elasticdev:::gcloud_simple_vpc
    arguments:
      vpc_name: project1
      gcloud_project: project1-288907
      credential_group: williaumwu:::gcloud_creds::project1
```
