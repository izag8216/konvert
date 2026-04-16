"""Tests for core converter engine."""

import json
import tempfile
from pathlib import Path

import pytest

from konvert.converter import ConverterError, convert, detect_input_schema


class TestConvertBasic:
    def test_json_to_yaml(self, json_file):
        result = convert(source=str(json_file), target_format="yaml")
        assert "name: konvert" in result

    def test_json_to_toml(self, json_file):
        result = convert(source=str(json_file), target_format="toml")
        assert "name" in result

    def test_yaml_to_json(self, yaml_file):
        result = convert(source=str(yaml_file), target_format="json")
        parsed = json.loads(result)
        assert parsed["name"] == "konvert"

    def test_toml_to_json(self, toml_file):
        result = convert(source=str(toml_file), target_format="json")
        parsed = json.loads(result)
        assert parsed["name"] == "konvert"

    def test_content_input(self, sample_json):
        result = convert(content=sample_json, target_format="yaml", input_format="json")
        assert "name: konvert" in result

    def test_auto_detect_input(self, json_file):
        result = convert(source=str(json_file), target_format="yaml")
        assert "name: konvert" in result


class TestConvertPretty:
    def test_pretty_json(self, json_file):
        result = convert(source=str(json_file), target_format="json", pretty=True)
        assert "\n" in result
        parsed = json.loads(result)
        assert parsed["name"] == "konvert"


class TestConvertErrors:
    def test_no_target_format(self):
        with pytest.raises(ConverterError, match="Target format"):
            convert(content="{}", target_format=None)

    def test_unsupported_target(self):
        with pytest.raises(ConverterError, match="Unsupported target"):
            convert(content="{}", target_format="xyz")

    def test_file_not_found(self):
        with pytest.raises(ConverterError, match="File not found"):
            convert(source="/nonexistent/file.json", target_format="yaml")

    def test_no_input(self):
        with pytest.raises(ConverterError, match="No input"):
            convert(target_format="json")

    def test_cannot_detect_format(self):
        with tempfile.NamedTemporaryFile(suffix=".xyz", mode="w", delete=False) as f:
            f.write("random text without structure")
            f.flush()
            with pytest.raises(ConverterError, match="Could not detect"):
                convert(source=f.name, target_format="json")


class TestSchemaDetection:
    def test_schema_from_file(self, json_file):
        result = detect_input_schema(source=str(json_file))
        assert result["type"] == "object"
        assert "name" in result["properties"]

    def test_schema_from_content(self, sample_json):
        result = detect_input_schema(content=sample_json, input_format="json")
        assert result["type"] == "object"


class TestAllFormatPairs:
    """Test that all format pairs produce valid output."""

    @pytest.fixture
    def data_file(self, tmp_dir):
        p = tmp_dir / "test.json"
        p.write_text('{"key": "value", "num": 42}', encoding="utf-8")
        return p

    def test_json_to_yaml(self, data_file):
        result = convert(source=str(data_file), target_format="yaml")
        assert "key: value" in result

    def test_json_to_toml(self, data_file):
        result = convert(source=str(data_file), target_format="toml")
        assert "key" in result

    def test_json_to_csv(self):
        content = '[{"name": "alice", "age": "30"}]'
        result = convert(content=content, target_format="csv", input_format="json")
        assert "name,age" in result

    def test_json_to_xml(self, data_file):
        result = convert(source=str(data_file), target_format="xml")
        assert "<key>value</key>" in result

    def test_json_to_ini(self, data_file):
        result = convert(source=str(data_file), target_format="ini")
        assert "key" in result

    def test_json_to_env(self, data_file):
        result = convert(source=str(data_file), target_format="env")
        assert "key=value" in result

    def test_yaml_to_json(self):
        content = "key: value\nnum: 42\n"
        result = convert(content=content, target_format="json", input_format="yaml")
        parsed = json.loads(result)
        assert parsed["key"] == "value"

    def test_toml_to_yaml(self):
        content = 'key = "value"\nnum = 42\n'
        result = convert(content=content, target_format="yaml", input_format="toml")
        assert "key: value" in result
