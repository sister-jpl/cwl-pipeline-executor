import json
import sys
import yaml
import os


def main(inputs_file):
    basedir = os.path.dirname(os.path.abspath(__file__))
    inputs = json.load(open(inputs_file, 'r'))
    workflow_inputs = {}
    # Expeting workflow_config to be a list of items
    workflow_config = inputs.get("workflow_config")
    if workflow_config is None:
        print("No workflow config provided, will not continue")
        exit(1)
    elif not isinstance(workflow_config, list):
        print(f"Workflow config should be a list {type(workflow_config)} provided, will not continue")
        exit(1)

    workflow_context = {}
    workflow_inputs = {}
    step_count = 1
    for step_config in workflow_config:
        if step_config.get("step_key"):
            workflow_inputs.update({f"step_{step_count}_key": step_config.get("step_key")})
            workflow_context.update({step_config.get("step_key"): step_config})
            step_count += 1
        else:
            raise RuntimeError("Workflow config missing step key for {}".format(step_config))

    workflow_context_file = "workflow_context.json"
    json.dump(workflow_context, open(workflow_context_file, 'w'))
    workflow_context_file = os.path.abspath(workflow_context_file)
    workflow_inputs.update({"workflow_context": {"class": "File", "path": workflow_context_file}})
    pge_prep_filepath = os.path.join(basedir, "workflow", "pge_prep.py")
    workflow_inputs.update({"pge_prep_filepath": pge_prep_filepath})
    run_pge_filepath = os.path.join(basedir, "workflow", "run_pge.py")
    workflow_inputs.update({"run_pge_filepath": run_pge_filepath})
    post_pge_filepath = os.path.join(basedir, "workflow", "post_pge.py")
    workflow_inputs.update({"post_pge_filepath": post_pge_filepath})

    workflow_inputs_file = "workflow-inputs.yml"
    yaml.dump(workflow_inputs, open(workflow_inputs_file, 'w'))


if __name__ == '__main__':
    main(sys.argv[1])
