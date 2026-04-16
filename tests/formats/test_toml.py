"""Tests for TOML format handler."""

import pytest

from konvert.formats.toml_fmt import TomlFormat


@pytest.fixture
def handler():
    return TomlFormat()


class TestTomlLoad:
    def test_load_basic(self, handler, sample_toml):
        result = handler.load(sample_toml)
        assert result["name"] == "konvert"
        assert result["version"] == "0.1.0"

    def test_load_nested_table(self, handler):
        data = "[section]\nkey = \"value\"\n"
        result = handler.load(data)
        assert result["section"]["key"] == "value"

    def test_load_preserves_comments(self, handler):
        data = "# This is a comment\nname = \"test\"\n"
        result = handler.load(data)
        assert result["name"] == "test"

    def test_load_array(self, handler):
        data = "items = [\"a\", \"b\", \"c\"]\n"
        result = handler.load(data)
        assert result["items"] == ["a", "b", "c"]


class TestTomlDump:
    def test_dump_basic(self, handler):
        data = {"name": "test", "version": "1.0"}
        result = handler.dump(data)
        assert "name" in result
        assert "test" in result

    def test_dump_nested(self, handler):
        data = {"section": {"key": "value"}}
        result = handler.dump(data)
        assert "[section]" in result
        assert "key" in result

    def test_roundtrip(self, handler, sample_toml):
        data = handler.load(sample_toml)
        output = handler.dump(data)
        restored = handler.load(output)
        assert dict(restored) == dict(data)
