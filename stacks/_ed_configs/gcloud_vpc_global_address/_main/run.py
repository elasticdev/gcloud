def run(stackargs):

    import json
    import os

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="gcloud_project")
    stack.parse.add_required(key="google_application_credentials",default="/var/tmp/share/.creds/gcloud.json")

    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")
    stack.parse.add_optional(key="global_address_prefix_length",default=20)

    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::global_address","global_address")
    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::networking_connection","networking_connection")

    # initialize variables
    stack.init_variables()

    # initialize exegroups for introspection and dependencies
    stack.init_execgroups()

    vpc_info = stack.get_resource(name=stack.vpc_name,
                                  resource_type="vpc",
                                  must_exists=True)[0]

    # global address
    global_address_state_id = stack.random_id(size=8)

    env_vars = {"NAME":global_address_state_id}

    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["TF_VAR_vpc_name"] = stack.vpc_name

    env_vars["GLOBAL_ADDRESS_NAME"] = "{}-{}".format(stack.vpc_name,"private-ip")
    env_vars["TF_VAR_global_addresss_name"] = "{}-{}".format(stack.vpc_name,"private-ip")

    env_vars["VPC_SELF_LINK"] = vpc_info["self_link"]
    env_vars["TF_VAR_vpc_self_link"] = vpc_info["self_link"]

    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["TF_VAR_gcloud_project"] = stack.gcloud_project

    env_vars["GLOBAL_ADDRESS_PREFIX_LENGTH"] = stack.global_address_prefix_length
    env_vars["TF_VAR_global_address_prefix_length"] = stack.global_address_prefix_length

    env_vars["STATEFUL_ID"] = global_address_state_id

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_compute_global_address"
    env_vars["RESOURCE_TYPE"] = "global_address"
    env_vars["RESOURCE_TAGS"] = [ "global_address", stack.vpc_name ]

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = "VPC_SELF_LINK,GCLOUD_PROJECT,VPC_NAME,GLOBAL_ADDRESS_NAME,GLOBAL_ADDRESS_PREFIX_LENGTH"

    inputargs = {"name":global_address_state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = global_address_state_id
    inputargs["human_description"] = 'Allocating global address for vpc "{}"'.format(stack.vpc_name)
    stack.global_address.insert(**inputargs)

    # networking connection
    networking_connection_state_id = stack.random_id(size=8)

    env_vars = {"NAME":networking_connection_state_id}

    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["TF_VAR_vpc_name"] = stack.vpc_name

    env_vars["GLOBAL_ADDRESS_NAME"] = "{}-{}".format(stack.vpc_name,"private-ip")
    env_vars["TF_VAR_global_addresss_name"] = "{}-{}".format(stack.vpc_name,"private-ip")

    env_vars["VPC_SELF_LINK"] = vpc_info["self_link"]
    env_vars["TF_VAR_vpc_self_link"] = vpc_info["self_link"]

    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["TF_VAR_gcloud_project"] = stack.gcloud_project

    env_vars["STATEFUL_ID"] = networking_connection_state_id

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_service_networking_connection"
    env_vars["RESOURCE_TYPE"] = "networking_connection"
    env_vars["RESOURCE_TAGS"] = [ "networking_connection", stack.vpc_name ]

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = "VPC_SELF_LINK,GCLOUD_PROJECT,VPC_NAME,GLOBAL_ADDRESS_NAME"

    inputargs = {"name":networking_connection_state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = networking_connection_state_id
    inputargs["human_description"] = 'Creating network connection/peering for vpc "{}"'.format(stack.vpc_name)
    stack.networking_connection.insert(**inputargs)

    return stack.get_results()
