import json
import sys

from src.cops_api import get_jobs
from src.utils import msg


def check(in_stream):
    input = json.load(in_stream)
    api_root = input["source"]["api_root"]
    status_id = input["source"].get("status_id")

    if not status_id:
        return [input["version"] or []]
    else:
        jobs = get_jobs(api_root)
        msg("jobs: {}", jobs)
        msg("Inputs: {}", input)

        jobs = [job for job in jobs if int(job["status_id"]) == status_id]

        if input["version"]:
            previous_id = input["version"]["id"]
            jobs = [job for job in jobs if int(job["id"]) > int(previous_id)]

        return [{"id": job["id"]} for job in jobs]


def main():
    print(json.dumps(check(sys.stdin)))


if __name__ == "__main__":
    main()
