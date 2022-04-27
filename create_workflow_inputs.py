import json
import sys
import yaml
import os


def main(inputs_file):
    basedir = os.path.dirname(os.path.abspath(__file__))
    inputs = json.load(open(inputs_file, 'r'))
    workflow_inputs = {}
    isofit_config = inputs.get("isofit_config", {})
    hytools_config = inputs.get("hytools_config", {})
    isofit_algorithm_key = "isofit"
    hytools_algorithm_key = "hytools"
    workflow_context = {isofit_algorithm_key: isofit_config,
                        hytools_algorithm_key: hytools_config}
    workflow_context_file = "workflow_context.json"
    json.dump(workflow_context, open(workflow_context_file, 'w'))
    workflow_context_file = os.path.abspath(workflow_context_file)
    workflow_inputs.update({"workflow_context": {"class": "File", "path": workflow_context_file}})
    workflow_inputs.update({"isofit_algorithm_key": isofit_algorithm_key})
    workflow_inputs.update({"hytools_algorithm_key": hytools_algorithm_key})

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
