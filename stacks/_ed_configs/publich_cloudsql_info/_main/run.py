def run(stackargs):

    # instantiate stack
    stack = newStack(stackargs)

    # add variables
    stack.parse.add_required(key="db_instance_name")
    stack.parse.add_required(key="db_root_user",default="null")
    stack.parse.add_required(key="db_root_password",default="null")
    stack.parse.add_required(key="gcloud_region",default="us-west1")
    stack.parse.add_required(key="database_version")

    # init the stack namespace
    stack.init_variables()

    database_info = stack.get_resource(name=stack.db_instance_name,
                                       resource_type="database",
                                       must_exists=True)[0]

    keys2pass = ['private_ip_address','connection_name']
    pipeline_env_var = stack.add_dict2dict(keys2pass,{},database_info,addNone=None)

    if stack.database_version:
        pipeline_env_var["{}_INSTANCE_NAME".format(stack.engine.upper())] = stack.db_instance_name
        pipeline_env_var["{}_ROOT_USER".format(stack.engine.upper())] = stack.db_root_user
        pipeline_env_var["{}_ROOT_PASSWORD".format(stack.engine.upper())] = stack.db_root_password
        pipeline_env_var["{}_HOST".format(stack.engine.upper())] = database_info["private_ip_address"]
        pipeline_env_var["{}_CONNECTION_NAME".format(stack.engine.upper())] = database_info["connection_name"]
        pipeline_env_var["{}_REGION".format(stack.engine.upper())] = stack.gcloud_region
    else:
        pipeline_env_var["DB_INSTANCE_NAME"] = stack.db_instance_name
        pipeline_env_var["DB_ROOT_USER"] = stack.db_root_user
        pipeline_env_var["DB_ROOT_PASSWORD"] = stack.db_root_password
        pipeline_env_var["DB_REGION"] = stack.gcloud_region
        pipeline_env_var["DB_HOST"] = database_info["private_ip_address"]
        pipeline_env_var["DB_CONNECTION_NAME"] = database_info["connection_name"]

    stack.add_host_env_vars_to_run(pipeline_env_var)
    stack.publish(pipeline_env_var,**stackargs)

    return stack.get_results()
