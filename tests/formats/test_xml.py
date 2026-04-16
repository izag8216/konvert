"""Tests for XML format handler."""

import pytest

from konvert.formats.xml_fmt import XmlFormat


@pytest.fixture
def handler():
    return XmlFormat()


class TestXmlLoad:
    def test_load_basic(self, handler, sample_xml):
        result = handler.load(sample_xml)
        assert result["root"]["name"] == "konvert"
        assert result["root"]["version"] == "0.1.0"

    def test_load_nested(self, handler):
        data = "<root><a><b>value</b></a></root>"
        result = handler.load(data)
        assert result["root"]["a"]["b"] == "value"


class TestXmlDump:
    def test_dump_basic(self, handler):
        data = {"root": {"name": "test"}}
        result = handler.dump(data)
        assert "<root>" in result
        assert "<name>test</name>" in result

    def test_dump_pretty(self, handler):
        data = {"root": {"name": "test"}}
        result = handler.dump(data, pretty=True)
        assert "\n" in result

    def test_dump_wraps_primitive(self, handler):
        result = handler.dump("hello")
        assert "hello" in result
