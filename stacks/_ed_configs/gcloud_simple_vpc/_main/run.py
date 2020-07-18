def run(stackargs):

    import json
    import os

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="gcloud_project")

    # credentials is more permanent, and will be used in other stacks - GOOGLE_APPLICATION_CREDENTIALS
    # this will use the google oauth access token that can be renewed in the UI after it expires
    stack.parse.add_required(key="google_application_credentials",default="/tmp/.credentials.json")

    # we set this to null to pass the introspection
    # ref 5490734650346
    stack.parse.add_required(key="credential_group")

    stack.parse.add_optional(key="gcloud_region",default="us-west1")

    # docker image to execute terraform with
    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")
    stack.parse.add_optional(key="public_cidr",default="10.10.10.0/24")
    stack.parse.add_optional(key="private_cidr",default="10.10.20.0/24")

    # initialize variables
    stack.init_variables()

    # declare execution groups
    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::firewall","firewall")
    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::subnets","subnets")
    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::vpc","vpc")

    # initialize exegroups for introspection and dependencies
    stack.init_execgroups()

    # ref 5490734650346
    stack.add_execgroup("elasticdev:::gcloud::base {} elasticdev:::gcloud::firewall".format(stack.credential_group),"firewall",overide=True)
    stack.add_execgroup("elasticdev:::gcloud::base {} elasticdev:::gcloud::subnets".format(stack.credential_group),"subnets",overide=True)
    stack.add_execgroup("elasticdev:::gcloud::base {} elasticdev:::gcloud::vpc".format(stack.credential_group),"vpc",overide=True)

    # we initialize exegroups a second time
    # to include credential_group
    stack.reset_execgroups()

    # CREATE EMPTY VPC
    vpc_state_id = stack.random_id(size=8)
    exec_dir = os.path.join("/tmp",vpc_state_id)

    env_vars = {"NAME":stack.vpc_name}
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(exec_dir,stack.google_application_credentials)
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    env_vars["RESOURCE_TYPE"] = "vpc"
    env_vars["RESOURCE_TAGS"] = [ "vpc", stack.vpc_name ]
    env_vars["RESOURCE_MAIN"] = True

    # determine what env vars to pass to 
    # the docker execution container
    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = ["GCLOUD_PROJECT", "VPC_NAME" ]

    inputargs = {"name":stack.vpc_name}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = vpc_state_id
    inputargs["chrootfiles_dest_dir"] = exec_dir
    inputargs["stateful_dir"] = exec_dir
    inputargs["exec_dir"] = exec_dir
    stack.vpc.insert(**inputargs)

    # CREATE SUBNETS
    subnet_state_id = stack.random_id(size=8)
    exec_dir = os.path.join("/tmp",subnet_state_id)

    env_vars = {"NAME":subnet_state_id}
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["GCLOUD_REGION"] = stack.gcloud_region
    env_vars["PUBLIC_CIDR"] = stack.public_cidr
    env_vars["PRIVATE_CIDR"] = stack.private_cidr
    env_vars["STATEFUL_ID"] = subnet_state_id

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(exec_dir,stack.google_application_credentials)
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    env_vars["RESOURCE_MAP_KEYS"] = "ip_cidr_range:cidr,provider:cloud_provider"
    env_vars["RESOURCE_TYPE"] = "subnet"
    env_vars["RESOURCE_TAGS"] = [ "subnet", stack.vpc_name ]

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = ["GCLOUD_PROJECT", "VPC_NAME", "PRIVATE_CIDR", "PUBLIC_CIDR", "GCLOUD_REGION" ]

    inputargs = {"name":subnet_state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = subnet_state_id
    inputargs["chrootfiles_dest_dir"] = exec_dir
    inputargs["stateful_dir"] = exec_dir
    inputargs["exec_dir"] = exec_dir
    stack.subnets.insert(**inputargs)

    # CREATE FIREWALL
    firewall_state_id = stack.random_id(size=8)
    exec_dir = os.path.join("/tmp",firewall_state_id)

    env_vars = {"NAME":firewall_state_id}
    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["PUBLIC_CIDR"] = stack.public_cidr
    env_vars["PRIVATE_CIDR"] = stack.private_cidr
    env_vars["STATEFUL_ID"] = firewall_state_id

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(exec_dir,stack.google_application_credentials)
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    env_vars["RESOURCE_TYPE"] = "firewall"
    env_vars["RESOURCE_TAGS"] = [ "firewall", stack.vpc_name ]

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = ["GCLOUD_PROJECT", "VPC_NAME", "PRIVATE_CIDR", "PUBLIC_CIDR" ]

    inputargs = {"name":firewall_state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = firewall_state_id
    inputargs["chrootfiles_dest_dir"] = exec_dir
    inputargs["stateful_dir"] = exec_dir
    inputargs["exec_dir"] = exec_dir
    stack.firewall.insert(**inputargs)

    return stack.get_results()
