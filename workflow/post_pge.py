import json
import argparse
import fnmatch


def match_products_to_params(context):
    output_json = dict()
    products = context.get("products", [])
    regex_filters = context.get("output_filter", None)
    if regex_filters:
        for param_name, match_pattern in regex_filters.items():
            for prod in products:
                if prod.startswith("s3://"):
                    if fnmatch.fnmatch(prod, match_pattern):
                        output_json[param_name] = prod
    return output_json


def main(context):
    """
    Example context:
    {
     "products": [
      "some-url.txt",
      "some-tar-file.tar"
     ],
     "output_filter": {"file":"*txt", "param": "*tar"}
    }
    :param context:
    :return:
    """
    # print(f"Filtering outputs {json.dumps(context, indent=1)}")
    # output_json = context
    # print(f"Output context from post pge {json.dumps(output_json, indent=1)}")
    # json.dump(output_json, open("post_pge_output_context.json", 'w'), indent=1)
    print("Currently post PGE step is a pass through")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PGE step')
    parser.add_argument("--input_context", dest="input_context", required=True)
    parser.add_argument("--algorithm_key", dest="algorithm_key", required=False, default="na")
    args = parser.parse_args()
    input_context_file = args.input_context
    algorithm_key = args.algorithm_key
    context = json.load(open(input_context_file, 'r'))
    main(context)
    json.dump(context, open(f"{algorithm_key}_post_pge_output_context.json", 'w'), indent=1)

