def run(stackargs):

    import json

    stack = newStack(stackargs)

    stack.parse.add_project(key="image_name")
    stack.parse.add_project(key="gcloud_project")

    stack.parse.add_optional(key="gcloud_src_dir",default="/var/tmp/docker/build")
    stack.parse.add_optional(key="gcloud_template_file_path",default="/var/tmp/docker/build/cloudbuild.yaml.ja2")
    stack.parse.add_optional(key="gcloud_config_file_path",default="/var/tmp/docker/build/cloudbuild.yaml")
    stack.parse.add_optional(key="google_application_credentials",default="/tmp/credentials.json")

    stack.add_shelloutconfig('elasticdev:::gcloud::container_builder',"container_builder")

    stack.init_variables()
    stack.init_shelloutconfigs()

    # Call to create the server with shellout script
    stack.env_vars = {"INSERT_IF_EXISTS":False}
    stack.env_vars["IMAGE_NAME"] = stack.image_name
    stack.env_vars["GCLOUD_PROJECT"] = stack.gcloud_project
    stack.env_vars["METHOD"] = "run"
    stack.env_vars["GCLOUD_SRC_DIR"] = stack.gcloud_src_dir
    stack.env_vars["GCLOUD_TEMPLATE_FILE_PATH"] = stack.gcloud_template_file_path
    stack.env_vars["GCLOUD_CONFIG_FILE_PATH"] = stack.gcloud_config_file_path
    stack.env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials

    if hasattr(stack,"job_instance_id") and stack.job_instance_id: stack.env_vars["JOB_INSTANCE_ID"] = stack.job_instance_id
    if hasattr(stack,"schedule_id") and stack.schedule_id: stack.env_vars["SCHEDULE_ID"] = stack.schedule_id

    inputargs = {"display":True}
    inputargs["human_description"] = 'Execute gcloud container build for image_name {}'.format(stack.image_name)
    inputargs["env_vars"] = json.dumps(stack.env_vars)
    inputargs["automation_phase"] = "build"
    inputargs["retries"] = 1
    inputargs["timeout"] = 60
    inputargs["wait_last_run"] = 5
    stack.container_builder.resource_exec(**inputargs)

    return stack.get_results()
