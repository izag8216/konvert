"""Tests for JSON format handler."""

import json

import pytest

from konvert.formats.json_fmt import JsonFormat


@pytest.fixture
def handler():
    return JsonFormat()


class TestJsonLoad:
    def test_load_object(self, handler, sample_json):
        result = handler.load(sample_json)
        assert result["name"] == "konvert"
        assert result["version"] == "0.1.0"
        assert result["features"] == ["json", "yaml"]

    def test_load_array(self, handler):
        result = handler.load("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_load_nested(self, handler):
        data = '{"a": {"b": {"c": 1}}}'
        result = handler.load(data)
        assert result["a"]["b"]["c"] == 1

    def test_load_unicode(self, handler):
        data = '{"greeting": "\\u3053\\u3093\\u306b\\u3061\\u306f"}'
        result = handler.load(data)
        assert result["greeting"] == "こんにちは"

    def test_load_empty_object(self, handler):
        result = handler.load("{}")
        assert result == {}


class TestJsonDump:
    def test_dump_compact(self, handler):
        data = {"name": "test"}
        result = handler.dump(data)
        assert result == '{"name": "test"}'

    def test_dump_pretty(self, handler):
        data = {"name": "test"}
        result = handler.dump(data, pretty=True)
        assert '"name": "test"' in result
        assert "\n" in result

    def test_dump_unicode(self, handler):
        data = {"greeting": "こんにちは"}
        result = handler.dump(data)
        assert "こんにちは" in result
        assert "\\u" not in result

    def test_dump_array(self, handler):
        data = [1, 2, 3]
        result = handler.dump(data)
        assert result == "[1, 2, 3]"

    def test_roundtrip(self, handler, sample_json):
        data = handler.load(sample_json)
        output = handler.dump(data)
        restored = handler.load(output)
        assert restored == data
