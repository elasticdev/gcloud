def run(stackargs):

    import json
    import os

    # instantiate authoring stack
    stack = newStack(stackargs)

    # name of the cloudsql database
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="gcloud_project")
    stack.parse.add_required(key="gcloud_region",default="us-west1")
    stack.parse.add_required(key="gcloud_zone",default="us-west1b")
    stack.parse.add_required(key="google_application_credentials",default="/var/tmp/share/.creds/gcloud.json")
    stack.parse.add_required(key="disk_size",default=10)
    stack.parse.add_required(key="instance_type",default="f1-micro")
    stack.parse.add_required(key="image",default="cos-cloud/cos-stable")

    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")
    stack.parse.add_optional(key="use_docker",default=True,null_allowed=True)

    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::cloud_sql_proxy","cloud_sql_proxy")

    # initialize variables
    stack.init_variables()
    stack.init_execgroups()

    # retrieve resources
    vpc_info = stack.get_resource(name=stack.vpc_name,
                                  resource_type="vpc",
                                  must_exists=True)[0]

    database_instance = stack.get_resource(name=stack.name,
                                           resource_type="database_instance",
                                           must_exists=True)[0]

    state_id = stack.random_id(size=8)

    env_vars = {"NAME":state_id}
    env_vars["TF_VAR_vpc_name"] = stack.vpc_name
    env_vars["TF_VAR_vpc_self_link"] = vpc_info["self_link"]
    env_vars["TF_VAR_gcloud_project"] = stack.gcloud_project

    env_vars["TF_VAR_gcloud_region"] = stack.gcloud_region
    env_vars["TF_VAR_gcloud_zone"] = stack.gcloud_zone
    env_vars["TF_VAR_instance_type"] = stack.instance_type
    env_vars["TF_VAR_disk_size"] = stack.disk_size
    env_vars["TF_VAR_image"] = stack.image
    env_vars["TF_VAR_cloudsql_name"] = stack.name
    env_vars["TF_VAR_cloudsql_connection_name"] = database_instance["connection_name"]
    env_vars["TF_VAR_stateful_id"] = state_id
    #env_vars["TF_VAR_service_account_email_address"] = database_instance["service_account_email_address"]

    env_vars["STATEFUL_ID"] = state_id
    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["METHOD"] = "create"
    if stack.use_docker: env_vars["use_docker".upper()] = True

    # if you use a plural terraform_resource_types, then it assume it contains
    # multiple terraform types to be placed in the resource database
    terraform_resource_types = {"google_compute_subnetwork":"subnet",
                                "google_compute_instance":"server",
                                "google_service_account_key":"service_account"}

    env_vars["TERRAFORM_RESOURCE_TYPES"] = json.dumps(terraform_resource_types)
    env_vars["RESOURCE_TAGS"] = "{},{},{},{}".format("cloud_sql_proxy","sql_proxy","proxy",stack.name)

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["TF_TEMPLATE_VARS"] = "GCLOUD_PRIVATE_KEY,GCLOUD_CLIENT_EMAIL"

    inputargs = {"name":state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = state_id
    inputargs["human_description"] = 'Executing Terraform to create cloud sql proxy on vpc "{}"'.format(stack.vpc_name)

    stack.cloud_sql_proxy.insert(**inputargs)

    return stack.get_results()
