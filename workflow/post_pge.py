import json
import argparse


def main(context):
    print(f"Filtering outputs {json.dumps(context, indent=1)}")
    # TODO RE match
    output_json = {"products": ["some-url.txt", "some-tar-file.tar"]}
    json.dump(output_json, open("post_pge_output_context.json", 'w'), indent=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PGE step')
    parser.add_argument("--input_context", dest="input_context", required=True)
    args = parser.parse_args()
    input_context_file = args.input_context
    context = json.load(open(input_context_file, 'r'))
    main(context)
