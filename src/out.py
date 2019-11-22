import os
import sys
import json

from src.event_api import update_event
from src.utils import msg


def out(src_path, in_stream):
    input = json.load(in_stream)
    data = input["params"]

    # Remove the id which represents the path in resource.
    # Keep the rest of the information to update the event.
    id_path = data.pop("id")

    msg("Input: {}", input)

    with open(os.path.join(src_path, id_path), "r") as infile:
        id = infile.read()

    pdf_url = data.get("pdf_url")
    if pdf_url:
        with open(os.path.join(src_path, pdf_url), "r") as infile:
            pdf_url = infile.read()
            data["pdf_url"] = pdf_url

    msg("Params: {}", data)
    msg(f"Updating status of event id {id}")

    response = update_event(input["source"]["api_root"], id, data)

    return {"version": {"id": response["id"]}}


def main():
    src_path = sys.argv[1]
    msg("Source dir {}", src_path)
    print(json.dumps(out(src_path, sys.stdin)))
