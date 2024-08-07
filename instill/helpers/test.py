import argparse
import json
import pprint

import requests

from instill.utils.logger import Logger

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input",
    help="inference input json",
    required=True,
)

args = parser.parse_args()

resp = requests.post("http://127.0.0.1:8000/", json=json.loads(args.input), timeout=600)

if resp.status_code == 200:
    Logger.i(f"[Instill] Outputs:\n{pprint.pformat(resp.json())}")
else:
    Logger.e(f"[Instill] Errors:\n{pprint.pformat(resp.text)}")
