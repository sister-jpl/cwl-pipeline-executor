import json
import argparse
import fnmatch


def prepare_context(input_contexts: []):
    products = []
    if type(input_contexts) is not list:
        input_contexts = [input_contexts]
    for context in input_contexts:
        with open(context) as c:
            json_context = json.load(c)
            products.extend(json_context.get("products", []))
    return {"products": products}


def filter_products(context: {}, input_filter: {}):
    output_json = dict()
    products = context.get("products", [])
    regex_filters = input_filter
    if regex_filters:
        for param_name, match_pattern in input_filter.items():
            for prod in products:
                if prod.startswith("s3://"):
                    if fnmatch.fnmatch(prod, match_pattern):
                        output_json[param_name] = prod
    return output_json


def main(workflow_context, context, algorithm_key):
    print(json.dumps(workflow_context))
    algorithm = workflow_context.get(algorithm_key, None)
    if algorithm:
        output_json = algorithm
        params = algorithm.get("params", {})
        # if not first step of workflow, pass necessary files to next step
        params.update(filter_products(context, algorithm.get("input_filter", {})))
        output_json.update({"params": params})
        print("Output Context: \n{}".format(json.dumps(output_json)))
        json.dump(output_json, open(f"{algorithm_key}_output_context.json", 'w'), indent=1)
        return output_json
    raise KeyError(f"Specified Algorithm {algorithm_key} not found in params")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PGE Preprocess step')
    parser.add_argument("--workflow_context", dest="workflow_context", required=True)
    parser.add_argument("--input_context", dest="input_context", default=[], nargs='*')
    parser.add_argument("--algorithm_key", dest="algorithm_key", required=True)
    args = parser.parse_args()
    global_context_file = args.workflow_context

    # input context will be empty for the first PGE in the workflow. It is
    context = prepare_context(args.input_context)
    algorithm_key = args.algorithm_key
    workflow_context = json.load(open(global_context_file, 'r'))
    main(workflow_context, context, algorithm_key)
