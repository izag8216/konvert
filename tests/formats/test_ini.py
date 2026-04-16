"""Tests for INI format handler."""

import pytest

from konvert.formats.ini_fmt import IniFormat


@pytest.fixture
def handler():
    return IniFormat()


class TestIniLoad:
    def test_load_basic(self, handler, sample_ini):
        result = handler.load(sample_ini)
        assert "metadata" in result
        assert result["metadata"]["name"] == "konvert"

    def test_load_multiple_sections(self, handler):
        data = "[section1]\nkey1 = val1\n[section2]\nkey2 = val2\n"
        result = handler.load(data)
        assert result["section1"]["key1"] == "val1"
        assert result["section2"]["key2"] == "val2"


class TestIniDump:
    def test_dump_basic(self, handler):
        data = {"section": {"key": "value"}}
        result = handler.dump(data)
        assert "[section]" in result
        assert "key = value" in result

    def test_dump_preserves_sections(self, handler, sample_ini):
        data = handler.load(sample_ini)
        output = handler.dump(data)
        assert "[metadata]" in output
