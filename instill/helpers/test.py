import argparse
import json
import pprint

import requests

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input",
    help="inference input json",
    required=True,
)

args = parser.parse_args()
pprint.pprint(
    requests.post(
        "http://127.0.0.1:8000/", json=json.loads(args.input), timeout=600
    ).text
)
