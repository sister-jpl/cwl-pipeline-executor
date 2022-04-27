import json
import argparse


def main(workflow_context, context, algorithm_key):
    print(json.dumps(workflow_context))
    algorithm = workflow_context.get(algorithm_key, None)
    if algorithm:
        output_json = algorithm
        params = algorithm.get("params", {})
        if context:
            # if not first step of workflow, pass necessary files to next step
            for param in context:
                params.update({param: context.get(param)})
        output_json.update({"params": params})
        json.dump(output_json, open("output_context.json", 'w'), indent=1)
        return output_json
    raise KeyError(f"Specified Algorithm {algorithm_key} not found in params")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PGE Preprocess step')
    parser.add_argument("--workflow_context", dest="workflow_context", required=True)
    parser.add_argument("--input_context", dest="input_context")
    parser.add_argument("--algorithm_key", dest="algorithm_key", required=True)
    args = parser.parse_args()
    global_context_file = args.workflow_context
    context = None
    # input context will be empty for the first PGE in the workflow. It is
    if args.input_context:
        input_context_file = args.input_context
        context = json.load(open(input_context_file, 'r'))
    algorithm_key = args.algorithm_key
    workflow_context = json.load(open(global_context_file, 'r'))
    main(workflow_context, context, algorithm_key)
