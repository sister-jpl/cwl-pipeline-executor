import json
import sys
import os

input_context_file = sys.argv[1]

context = json.load(open(input_context_file, 'r'))
print(json.dumps(context))
output_json = {"key": "Value"}
output_json.update(context)
json.dump(output_json, open("output_context.json", 'w'))
