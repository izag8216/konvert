"""Tests for YAML format handler."""

import pytest

from konvert.formats.yaml_fmt import YamlFormat


@pytest.fixture
def handler():
    return YamlFormat()


class TestYamlLoad:
    def test_load_basic(self, handler, sample_yaml):
        result = handler.load(sample_yaml)
        assert result["name"] == "konvert"
        assert result["version"] == "0.1.0"
        assert result["features"] == ["json", "yaml"]

    def test_load_empty(self, handler):
        result = handler.load("")
        assert result == {}

    def test_load_nested(self, handler):
        data = "a:\n  b:\n    c: 1\n"
        result = handler.load(data)
        assert result["a"]["b"]["c"] == 1

    def test_load_unicode(self, handler):
        data = "greeting: こんにちは\n"
        result = handler.load(data)
        assert result["greeting"] == "こんにちは"


class TestYamlDump:
    def test_dump_basic(self, handler):
        data = {"name": "test"}
        result = handler.dump(data)
        assert "name: test" in result

    def test_dump_list(self, handler):
        data = {"items": ["a", "b", "c"]}
        result = handler.dump(data)
        assert "- a" in result
        assert "- b" in result

    def test_dump_unicode(self, handler):
        data = {"greeting": "こんにちは"}
        result = handler.dump(data)
        assert "こんにちは" in result

    def test_roundtrip(self, handler, sample_yaml):
        data = handler.load(sample_yaml)
        output = handler.dump(data)
        restored = handler.load(output)
        assert restored == data
