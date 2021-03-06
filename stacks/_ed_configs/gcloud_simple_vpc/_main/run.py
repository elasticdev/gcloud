def run(stackargs):

    import json
    import os

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="gcloud_project")

    # this will set the GOOGLE_APPLICATION_CREDENTIALS environment variable relative to the shared docker volume
    # it should be in the directory /var/tmp/terraform
    stack.parse.add_required(key="google_application_credentials",default="/var/tmp/share/.creds/gcloud.json")
    stack.parse.add_required(key="auto_create_subnetworks",default="null")
    stack.parse.add_required(key="global_address_block",default="null")

    # docker image to execute terraform with
    stack.parse.add_optional(key="gcloud_region",default="us-west1")
    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")
    stack.parse.add_optional(key="public_cidr",default="10.10.10.0/24")
    stack.parse.add_optional(key="private_cidr",default="10.10.20.0/24")
    stack.parse.add_optional(key="global_address_prefix_length",default=20)
    stack.parse.add_optional(key="use_docker",default=True,null_allowed=True)

    stack.add_substack('elasticdev:::gcloud_vpc_global_address')

    # initialize variables
    stack.init_variables()
    stack.init_substacks()

    # declare execution groups
    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::firewall","firewall")
    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::subnets","subnets")
    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::vpc","vpc")

    # initialize exegroups for introspection and dependencies
    stack.init_execgroups()

    null_values = [ None, "None", False, "false"]

    # CREATE EMPTY VPC
    vpc_state_id = stack.random_id(size=8)

    env_vars = {"NAME":stack.vpc_name}

    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["TF_VAR_gcloud_project"] = stack.gcloud_project

    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["TF_VAR_vpc_name"] = stack.vpc_name

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["METHOD"] = "create"
    if stack.use_docker: env_vars["use_docker".upper()] = True

    env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_compute_network"
    env_vars["RESOURCE_TYPE"] = "vpc"
    env_vars["RESOURCE_TAGS"] = 'vpc,{}'.format(stack.vpc_name)

    if stack.auto_create_subnetworks not in null_values:
        env_vars["AUTO_CREATE_SUBNETWORKS"] = "true"
        env_vars["TF_VAR_auto_create_subnetworks"] = "true"

    #env_vars["RESOURCE_PARENT"] = True

    # determine what env vars to pass to 
    # the docker execution container
    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["TF_TEMPLATE_VARS"] = "GCLOUD_PROJECT,VPC_NAME" 

    inputargs = {"name":stack.vpc_name}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = vpc_state_id
    inputargs["human_description"] = 'Creating vpc "{}"'.format(stack.vpc_name)
    stack.vpc.insert(**inputargs)

    # if auto create subnets is not True, then we need to 
    # explicity specify the subnets
    # CREATE SUBNETS
    if stack.auto_create_subnetworks in null_values:

        subnet_state_id = stack.random_id(size=8)

        env_vars = {"NAME":subnet_state_id}
        env_vars["STATEFUL_ID"] = subnet_state_id

        env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
        env_vars["TF_VAR_gcloud_project"] = stack.gcloud_project

        env_vars["VPC_NAME"] = stack.vpc_name
        env_vars["TF_VAR_vpc_name"] = stack.vpc_name

        env_vars["GCLOUD_REGION"] = stack.gcloud_region
        env_vars["TF_VAR_gcloud_region"] = stack.gcloud_region

        env_vars["PUBLIC_CIDR"] = stack.public_cidr
        env_vars["TF_VAR_public_cidr"] = stack.public_cidr

        env_vars["PRIVATE_CIDR"] = stack.private_cidr
        env_vars["TF_VAR_private_cidr"] = stack.private_cidr

        env_vars["AUTO_CREATE_SUBNETWORKS"] = "false"
        env_vars["TF_VAR_auto_create_subnetworks"] = "false"

        env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
        env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
        env_vars["METHOD"] = "create"
        if stack.use_docker: env_vars["use_docker".upper()] = True

        env_vars["RESOURCE_MAP_KEYS"] = "ip_cidr_range:cidr,provider:cloud_provider"
        env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_compute_subnetwork"
        env_vars["RESOURCE_TYPE"] = "subnet"
        env_vars["RESOURCE_TAGS"] = 'subnet,{}'.format(stack.vpc_name)

        docker_env_fields_keys = env_vars.keys()
        docker_env_fields_keys.remove("METHOD")
        env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
        env_vars["TF_TEMPLATE_VARS"] = "GCLOUD_PROJECT,VPC_NAME,PRIVATE_CIDR,PUBLIC_CIDR,GCLOUD_REGION"

        inputargs = {"name":subnet_state_id}
        inputargs["env_vars"] = json.dumps(env_vars)
        inputargs["stateful_id"] = subnet_state_id
        inputargs["human_description"] = 'Creating subnets on vpc "{}"'.format(stack.vpc_name)
        stack.subnets.insert(**inputargs)

    # if global_address is true, then we create the global_address 
    # parameters
    if stack.global_address_block not in null_values:

        # call substack for global_address since we need to look up self-link
        default_values = {"vpc_name":stack.vpc_name}
        default_values["gcloud_project"] = stack.gcloud_project
        default_values["global_address_prefix_length"] = stack.global_address_prefix_length
        default_values["google_application_credentials"] = stack.google_application_credentials
        default_values["docker_exec_env"] = stack.docker_exec_env
        stack.gcloud_vpc_global_address.insert(**{"default_values":default_values})

    # CREATE FIREWALL
    firewall_state_id = stack.random_id(size=8)

    env_vars = {"NAME":firewall_state_id}

    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["TF_VAR_vpc_name"] = stack.vpc_name

    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["TF_VAR_gcloud_project"] = stack.gcloud_project

    env_vars["PUBLIC_CIDR"] = stack.public_cidr
    env_vars["TF_VAR_public_cidr"] = stack.public_cidr

    env_vars["PRIVATE_CIDR"] = stack.private_cidr
    env_vars["TF_VAR_private_cidr"] = stack.private_cidr

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["METHOD"] = "create"
    if stack.use_docker: env_vars["use_docker".upper()] = True

    env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_compute_firewall"
    env_vars["RESOURCE_TYPE"] = "firewall"
    env_vars["RESOURCE_TAGS"] = 'firewall,{}'.format(stack.vpc_name)

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["TF_TEMPLATE_VARS"] = "GCLOUD_PROJECT,VPC_NAME,PRIVATE_CIDR,PUBLIC_CIDR"

    inputargs = {"name":firewall_state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = firewall_state_id
    inputargs["human_description"] = 'Creating firewall rules on vpc "{}"'.format(stack.vpc_name)
    stack.firewall.insert(**inputargs)

    return stack.get_results()
