"""Tests for format auto-detection."""

import pytest

from konvert.detector import detect_from_content, detect_from_extension, detect_schema


class TestExtensionDetection:
    def test_json(self):
        assert detect_from_extension("data.json") == "json"

    def test_yaml(self):
        assert detect_from_extension("config.yaml") == "yaml"

    def test_yml_alias(self):
        assert detect_from_extension("config.yml") == "yaml"

    def test_toml(self):
        assert detect_from_extension("pyproject.toml") == "toml"

    def test_csv(self):
        assert detect_from_extension("data.csv") == "csv"

    def test_xml(self):
        assert detect_from_extension("data.xml") == "xml"

    def test_ini(self):
        assert detect_from_extension("config.ini") == "ini"

    def test_env(self):
        assert detect_from_extension(".env") == "env"

    def test_unknown(self):
        assert detect_from_extension("data.xyz") is None

    def test_case_insensitive(self):
        assert detect_from_extension("DATA.JSON") == "json"


class TestContentDetection:
    def test_json_object(self):
        assert detect_from_content('{"key": "value"}') == "json"

    def test_json_array(self):
        assert detect_from_content("[1, 2, 3]") == "json"

    def test_xml(self):
        assert detect_from_content("<root><item>test</item></root>") == "xml"

    def test_xml_with_declaration(self):
        assert detect_from_content('<?xml version="1.0"?><root/>') == "xml"

    def test_empty(self):
        assert detect_from_content("") is None

    def test_toml(self):
        content = '[section]\nkey = "value"\n'
        assert detect_from_content(content) == "toml"

    def test_env(self):
        content = "DATABASE_URL=postgres://localhost\nPORT=5432\n"
        assert detect_from_content(content) == "env"

    def test_ini(self):
        content = "[database]\nhost = localhost\n"
        assert detect_from_content(content) == "ini"

    def test_csv(self):
        content = "name,age,city\nalice,30,Tokyo\nbob,25,Osaka\n"
        assert detect_from_content(content) == "csv"

    def test_yaml_key_value(self):
        content = "name: test\nversion: 1.0\n"
        assert detect_from_content(content) == "yaml"


class TestSchemaDetection:
    def test_string(self):
        assert detect_schema("hello") == {"type": "string"}

    def test_integer(self):
        assert detect_schema(42) == {"type": "integer"}

    def test_boolean(self):
        assert detect_schema(True) == {"type": "boolean"}

    def test_none(self):
        assert detect_schema(None) == {"type": "null"}

    def test_list(self):
        result = detect_schema([1, 2, 3])
        assert result["type"] == "array"
        assert result["length"] == 3

    def test_dict(self):
        result = detect_schema({"name": "test", "count": 5})
        assert result["type"] == "object"
        assert "name" in result["properties"]
        assert result["properties"]["name"] == {"type": "string"}
        assert result["properties"]["count"] == {"type": "integer"}

    def test_nested(self):
        data = {"config": {"db": {"host": "localhost"}}}
        result = detect_schema(data)
        assert result["type"] == "object"
        assert result["properties"]["config"]["properties"]["db"]["properties"]["host"] == {"type": "string"}
