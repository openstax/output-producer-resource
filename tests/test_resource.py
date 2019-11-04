import io
import json
import os
import tempfile

import vcr

from src import check, in_

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "data")


def read_file(filepath):
    with open(filepath, "r") as infile:
        return infile.read()


def make_stream(json_obj):
    stream = io.StringIO()
    json.dump(json_obj, stream)
    stream.seek(0)
    return stream


def make_input(version, **kwargs):
    payload = {"source": {
        "api_root": "https://cc1.cnx.org/api",
    },
        "version": version,
    }
    payload["source"].update(kwargs)

    return payload


def make_input_stream(version, **kwargs):
    return make_stream(make_input(version, **kwargs))


class TestCheck(object):

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_edge_case_queued_events(self):
        version = None

        in_stream = make_input_stream(version, status_id=1)
        result = check.check(in_stream)

        assert result == [{'id': '6'}, {'id': '7'}, {'id': '9'}, {'id': '10'}, {'id': '11'}]

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_edge_case_queued_no_events(self):
        version = None

        in_stream = make_input_stream(version, status_id=5)
        result = check.check(in_stream)

        assert result == []

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_has_newest_event(self):
        version = {"id": 10}

        in_stream = make_input_stream(version, status_id=1)
        result = check.check(in_stream)

        assert result == [{"id": "11"}]

    @vcr.use_cassette("tests/cassettes/test_check.yaml")
    def test_has_newer_events(self):
        version = {"id": 9}

        in_stream = make_input_stream(version, status_id=1)
        result = check.check(in_stream)

        assert result == [{'id': '10'}, {'id': '11'}]


class TestIn(object):
    @vcr.use_cassette('tests/cassettes/test_in.yaml')
    def test_resource_files_are_written(self):
        id = "1"
        version = {"version": {"id": id}}
        dest_path = tempfile.mkdtemp()

        in_stream = make_input_stream(version["version"])

        result = in_.in_(dest_path, in_stream)
        assert result == version

        event_id = read_file(os.path.join(dest_path, "id"))
        assert event_id == version["version"]["id"]

        event_json = read_file(os.path.join(dest_path, "event.json"))
        assert event_json == read_file(os.path.join(DATA_DIR, "event.json"))

        collection_id = read_file(os.path.join(dest_path, "collection_id"))
        assert collection_id == read_file(os.path.join(DATA_DIR, "collection_id"))

        collection_version = read_file(os.path.join(dest_path, "version"))
        assert collection_version == read_file(os.path.join(DATA_DIR, "version"))

        content_server = read_file(os.path.join(dest_path, "content_server"))
        assert content_server == read_file(os.path.join(DATA_DIR, "content_server"))
