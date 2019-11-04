import json
import os
import sys

from src import event_api as api
from src.utils import msg, write_file


def in_(dest_path, in_stream):
    input = json.load(in_stream)
    msg("Input: {}", input)

    api_root = input["source"]["api_root"]
    event_id = input["version"]["id"]

    event = api.get_event(api_root, event_id)
    msg("Event Returned: {}", event)

    collection_id = event["collection_id"]
    collection_version = event["version"] or "latest"
    content_server = event["content_server"]["hostname"]

    # Write out files
    write_file(os.path.join(dest_path, "id"), event_id)
    write_file(os.path.join(dest_path, "collection_id"), collection_id)
    write_file(os.path.join(dest_path, "version"), collection_version)
    write_file(os.path.join(dest_path, "content_server"), content_server)
    write_file(os.path.join(dest_path, "event.json"), event)

    return {"version": {"id": event_id}}


def main():
    dest_path = sys.argv[1]
    msg("Output dir {}", dest_path)
    version = in_(dest_path, sys.stdin)
    print(json.dumps(version))


if __name__ == '__main__':
    main()
