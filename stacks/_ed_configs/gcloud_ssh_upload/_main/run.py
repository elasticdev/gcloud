def run(stackargs):

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="name")
    stack.parse.add_required(key="ssh_user",default="root")
    stack.parse.add_required(key="gcloud_project")

    # add substacks
    stack.add_substack('elasticdev:::gcloud_ssh_upload_stage_2')

    # Initialize Variables in stack
    stack.init_variables()
    stack.init_substacks()

    # Create key
    cmd = "ssh_key create"
    order_type = "create-ssh_key::api"
    role = "cloud/credentials"

    default_values = {"name":stack.name}
    human_description = "Generate new ssh_key {} if it does not exists".format(stack.name)

    stack.insert_builtin_cmd(cmd,
                             order_type=order_type,
                             role=role,
                             human_description=human_description,
                             display=True,
                             default_values=default_values)

    return stack.get_results()
