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
    stack.parse.add_optional(key="private_ip_prefix_length",default=20)

    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::private_ip","private_ip")

    # initialize variables
    stack.init_variables()

    # initialize exegroups for introspection and dependencies
    stack.init_execgroups()

    # call stack for private_ip since we need to 
    # look up self-link
    vpc_info = stack.get_resource(name=stack.vpc_name,
                                  resource_type="vpc",
                                  must_exists=True)[0]

    state_id = stack.random_id(size=8)

    env_vars = {"NAME":state_id}
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["VPC_SELF_LINK"] = vpc_info["self_link"]
    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["PRIVATE_IP_PREFIX_LENGTH"] = stack.private_ip_prefix_length
    env_vars["STATEFUL_ID"] = state_id

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_compute_private_ip"
    env_vars["RESOURCE_TYPE"] = "private_ip"
    env_vars["RESOURCE_TAGS"] = [ "private_ip", stack.vpc_name ]

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = "VPC_SELF_LINK,GCLOUD_PROJECT,VPC_NAME,PRIVATE_IP_PREFIX_LENGTH"

    inputargs = {"name":state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = state_id
    stack.private_ip.insert(**inputargs)

    return stack.get_results()
