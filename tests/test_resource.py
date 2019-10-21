import io
import json
import os
from unittest import mock

import vcr

from src import check


def read_json_file(filepath):
    with open(filepath) as infile:
        return json.load(infile)


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
