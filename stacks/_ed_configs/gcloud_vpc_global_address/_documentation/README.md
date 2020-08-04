**Description**

  - This stack creates global_address space for an existing vpc on gcp

**Required**

| argument      | description                            | var type | default      |
| ------------- | -------------------------------------- | -------- | ------------ |
| vpc_name   | name of the vpc                 | string   | None         |
| gcloud_project      | the project id in gclouod from      | string   | None         |
| google_application_credentials      | the location for the json file gcp      | string     | /tmp/.credentials.json         |

**Optional**

| *argument*           | *description*                            | *var type* |  *default*      |
| ------------- | -------------------------------------- | -------- | ------------ |
| docker_exec_env      | docker container to execute terraform templates    | string   | elasticdev/terraform-run-env         |
| global_address_prefix_length      | private ip prefix length    | integer   | 20         |
