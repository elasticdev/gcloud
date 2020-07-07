def default():
    
    task = {}
    env_vars = []
    shelloutconfigs = []

    # This can be overided by env_vars in the resource add
    shelloutconfigs.append('elasticdev:::terraform::resource_wrapper')

    task['method'] = 'shelloutconfig'
    task['metadata'] = {'env_vars': env_vars,
                        'shelloutconfigs': shelloutconfigs
                        }

    return task
