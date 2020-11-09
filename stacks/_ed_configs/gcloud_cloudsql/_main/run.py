def run(stackargs):

    import json
    import os

    # instantiate authoring stack
    stack = newStack(stackargs)

    stack.parse.add_required(key="name")
    stack.parse.add_required(key="vpc_name")
    stack.parse.add_required(key="gcloud_project")
    stack.parse.add_required(key="gcloud_region",default="us-west1")
    stack.parse.add_required(key="google_application_credentials",default="/var/tmp/share/.creds/gcloud.json")
    stack.parse.add_required(key="database_version",default="POSTGRES_11")
    stack.parse.add_required(key="database_tier",default="db-f1-micro")
    stack.parse.add_required(key="availability_type",default="REGIONAL")
    stack.parse.add_required(key="disk_size",default=10)
    stack.parse.add_required(key="db_root_user",default="null")
    stack.parse.add_required(key="db_root_password",default="null")
    stack.parse.add_required(key="ipv4_enabled",default="null")

    stack.parse.add_optional(key="docker_exec_env",default="elasticdev/terraform-run-env")

    stack.add_execgroup("elasticdev:::gcloud::base elasticdev:::gcloud::cloudsql","cloudsql")
    stack.add_substack('elasticdev:::publish_cloudsql_info')

    # initialize variables
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    if not stack.db_root_user: 
        stack.set_variable("db_root_user",stack.get_random_string())

    if not stack.db_root_password: 
        stack.set_variable("db_root_password",stack.get_random_string())

    vpc_info = stack.get_resource(name=stack.vpc_name,
                                  resource_type="vpc",
                                  must_exists=True)[0]

    state_id = stack.random_id(size=8)

    env_vars = {"NAME":state_id}

    env_vars["VPC_NAME"] = stack.vpc_name
    env_vars["TF_VAR_vpc_name"] = stack.vpc_name

    env_vars["VPC_SELF_LINK"] = vpc_info["self_link"]
    env_vars["TF_VAR_vpc_self_link"] = vpc_info["self_link"]

    env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    env_vars["TF_VAR_gcloud_project"] = stack.gcloud_project

    env_vars["GCLOUD_REGION"] = stack.gcloud_region
    env_vars["TF_VAR_gcloud_region"] = stack.gcloud_region

    env_vars["CLOUDSQL_NAME"] = stack.name
    env_vars["TF_VAR_cloudsql_name"] = stack.name

    env_vars["DATABASE_VERSION"] = stack.database_version
    env_vars["TF_VAR_database_version"] = stack.database_version

    env_vars["DATABASE_TIER"] = stack.database_tier
    env_vars["TF_VAR_database_tier"] = stack.database_tier

    env_vars["AVAILABILITY_TYPE"] = stack.availability_type
    env_vars["TF_VAR_availability_type"] = stack.availability_type
    
    env_vars["DISK_SIZE"] = stack.disk_size
    env_vars["TF_VAR_disk_size"] = stack.disk_size

    env_vars["DB_ROOT_USER"] = stack.db_root_user
    env_vars["TF_VAR_db_root_user"] = stack.db_root_user

    env_vars["DB_ROOT_PASSWORD"] = stack.db_root_password
    env_vars["TF_VAR_db_root_password"] = stack.db_root_password

    if stack.ipv4_enabled:
        env_vars["IPV4_enabled"] = "true"
        env_vars["TF_VAR_ipv4_enabled"] = "true"

    env_vars["STATEFUL_ID"] = state_id

    env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    env_vars["DOCKER_EXEC_ENV"] = stack.docker_exec_env
    env_vars["USE_DOCKER"] = True
    env_vars["METHOD"] = "create"

    #env_vars["TERRAFORM_RESOURCE_TYPE"] = "google_sql_database"
    #env_vars["RESOURCE_TYPE"] = "database"

    # if you use a plural terraform_resource_types, then it assume it contains
    # multiple terraform types to be placed in the resource database
    env_vars["TERRAFORM_RESOURCE_TYPES"] = json.dumps({"google_sql_database":"database", "google_sql_database_instance":"database_instance"})
    env_vars["RESOURCE_TAGS"] = "{},{},{}".format("cloud_sql","database",stack.name)

    docker_env_fields_keys = env_vars.keys()
    docker_env_fields_keys.remove("METHOD")
    env_vars["DOCKER_ENV_FIELDS"] = ",".join(docker_env_fields_keys)
    env_vars["OS_TEMPLATE_VARS"] = "VPC_NAME,VPC_SELF_LINK,GCLOUD_PROJECT,GCLOUD_REGION,CLOUDSQL_NAME,DATABASE_VERSION,DATABASE_TIER,AVAILABILITY_TYPE,DISK_SIZE,DB_ROOT_USER,DB_ROOT_PASSWORD,IPV4_enabled,STATEFUL_ID"

    inputargs = {"name":state_id}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["stateful_id"] = state_id
    inputargs["human_description"] = 'Creating cloudsql "{}" on vpc "{}"'.format(stack.name,stack.vpc_name)

    stack.cloudsql.insert(**inputargs)

    # Insert variables into pipeline run
    overide_values = {"db_instance_name":stack.name}
    overide_values["db_root_user"] = stack.db_root_user
    overide_values["db_root_password"] = stack.db_root_password
    overide_values["database_version"] = stack.database_version
    overide_values["gcloud_region"] = stack.gcloud_region

    inputargs = {"overide_values":overide_values}
    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = 'Publish info for cloudsql"{}"'.format(stack.name)
    stack.publish_cloudsql_info.insert(display=True,**inputargs)

    return stack.get_results()
