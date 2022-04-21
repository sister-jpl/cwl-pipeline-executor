import json
import argparse


def main(context):
    print(f"Running algorithm with params {json.dumps(context, indent=1)}")
    output_json = {"products": ["some-url.txt", "some-tar-file.tar"]}
    output_json.update({"output_filter": context.get("output_filter", "")})
    json.dump(output_json, open("output_context.json", 'w'), indent=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PGE step')
    parser.add_argument("--input_context", dest="input_context", required=True)
    args = parser.parse_args()
    input_context_file = args.input_context
    context = json.load(open(input_context_file, 'r'))
    main(context)
