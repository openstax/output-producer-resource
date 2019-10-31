import json
import os
import sys

from src import event_api as api
from src.utils import msg


def in_(dest_path, in_stream):
    input = json.load(in_stream)
    msg("Input: {}", input)

    api_root = input["source"]["api_root"]
    event_id = input["version"]["id"]

    event = api.get_event(api_root, event_id)
    msg("Event Returned: {}", event)

    content_server = event["content_server"]["hostname"]

    # Write out files
    with open(os.path.join(dest_path, "id"), "w") as file:
        file.write(str(event_id))

    with open(os.path.join(dest_path, "collection_id"), "w") as file:
        file.write(event["collection_id"])

    with open(os.path.join(dest_path, "content_server"), "w") as file:
        file.write(content_server)

    with open(os.path.join(dest_path, "event.json"), "w") as file:
        json.dump(event, file)

    return {"version": {"id": event_id}}


def main():
    dest_path = sys.argv[1]
    msg("Output dir {}", dest_path)
    version = in_(dest_path, sys.stdin)
    print(json.dumps(version))


if __name__ == '__main__':
    main()
