import json
import argparse


def main(workflow_context, context, algorithm_key):
    print(json.dumps(context))
    algorithm = workflow_context.get(algorithm_key, None)
    if algorithm:
        output_json = algorithm
        params = algorithm.get("params", {})
        if context:
            products = context.get("products", [])
            params.update({"input_files": products})
        output_json.update({"params": params})
        json.dump(output_json, open("output_context.json", 'w'), indent=1)
        return
    raise KeyError(f"Specified Algorithm {algorithm_key} not found in params")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PGE Preprocess step')
    parser.add_argument("--workflow_context", dest="workflow_context", required=True)
    parser.add_argument("--input_context", dest="input_context")
    parser.add_argument("--algorithm_key", dest="algorithm_key", required=True)
    args = parser.parse_args()
    global_context_file = args.workflow_context
    context = None
    if args.input_context:
        input_context_file = args.input_context
        context = json.load(open(input_context_file, 'r'))
    algorithm_key = args.algorithm_key
    workflow_context = json.load(open(global_context_file, 'r'))
    main(workflow_context, context, algorithm_key)
