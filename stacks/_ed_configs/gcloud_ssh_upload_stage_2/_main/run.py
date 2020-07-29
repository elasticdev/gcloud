def run(stackargs):

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="ssh_user",default="root")
    stack.parse.add_required(key="gcloud_project")
    stack.parse.add_required(key="google_application_credentials",default="/var/tmp/share/.creds/gcloud.json")

    # add shelloutconfigs
    stack.add_shelloutconfig('elasticdev:::gcloud::docker-exec-metadata-ssh-keys',"shellout")

    # Initialize Variables in stack
    stack.init_variables()
    stack.init_shelloutconfigs()

    # Call to create the server with shellout script
    public_key = stack.get_ssh_key(name=stack.name)["public_key"]

    stack.env_vars = {"GCLOUD_PROJECT":stack.gcloud_project}
    stack.env_vars["GOOGLE_APPLICATION_CREDENTIALS"] = stack.google_application_credentials
    stack.env_vars["GCLOUD_SSH_KEYS"] = "{}:{}".format(stack.ssh_user,public_key)
    stack.env_vars["METHOD"] = "run"

    inputargs = {"env_vars":stack.env_vars}

    stack.shellout.run(**inputargs)

    #jiffy resource add shelloutconfig=$SCRIPT insert_env_vars='["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]' 
    #env_vars='{"AWS_DEFAULT_REGION":"us-east-1","METHOD":"create","NAME":"test", "PUBLIC_KEY":"ssh-rsa"}' 
    #GCLOUD_SSH_KEYS

    return stack.get_results()
