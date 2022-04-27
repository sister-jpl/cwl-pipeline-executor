import json
import sys


def main():
    context_file = "_context.json"
    context = json.load(open(context_file, 'r'))
    print(json.dumps(context, indent=2))
    sys.exit(1)


if __name__ == '__main__':
    main()
