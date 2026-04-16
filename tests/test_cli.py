"""Tests for CLI interface."""

import json
import tempfile
from pathlib import Path

import pytest

from click.testing import CliRunner

from konvert.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def json_file(tmp_dir):
    p = tmp_dir / "sample.json"
    p.write_text('{"name": "konvert", "version": "0.1.0"}', encoding="utf-8")
    return p


@pytest.fixture
def yaml_file(tmp_dir):
    p = tmp_dir / "sample.yaml"
    p.write_text("name: konvert\nversion: 0.1.0\n", encoding="utf-8")
    return p


class TestBasicConversion:
    def test_json_to_yaml(self, runner, json_file):
        result = runner.invoke(main, [str(json_file), "yaml"])
        assert result.exit_code == 0
        assert "name: konvert" in result.output

    def test_json_to_toml(self, runner, json_file):
        result = runner.invoke(main, [str(json_file), "toml"])
        assert result.exit_code == 0
        assert "name" in result.output

    def test_using_to_flag(self, runner, json_file):
        result = runner.invoke(main, [str(json_file), "--to", "yaml"])
        assert result.exit_code == 0
        assert "name: konvert" in result.output

    def test_yaml_to_json(self, runner, yaml_file):
        result = runner.invoke(main, [str(yaml_file), "json"])
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert parsed["name"] == "konvert"


class TestPipeMode:
    def test_stdin_pipe(self, runner):
        result = runner.invoke(main, ["-", "yaml"], input='{"key": "value"}')
        assert result.exit_code == 0
        assert "key: value" in result.output


class TestPrettyPrint:
    def test_pretty_json(self, runner, json_file):
        result = runner.invoke(main, [str(json_file), "json", "--pretty"])
        assert result.exit_code == 0
        assert "\n" in result.output


class TestSchemaDetection:
    def test_schema_flag(self, runner, json_file):
        result = runner.invoke(main, [str(json_file), "--schema"])
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert parsed["type"] == "object"


class TestInPlace:
    def test_inplace_conversion(self, runner, tmp_dir):
        src = tmp_dir / "config.yaml"
        src.write_text("name: test\n", encoding="utf-8")
        result = runner.invoke(main, [str(src), "--to", "json", "--in-place"])
        assert result.exit_code == 0
        assert (tmp_dir / "config.json").exists()
        assert not src.exists()


class TestOutput:
    def test_output_file(self, runner, json_file, tmp_dir):
        out = tmp_dir / "output.yaml"
        result = runner.invoke(main, [str(json_file), "yaml", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        assert "name: konvert" in out.read_text()


class TestVersionAndHelp:
    def test_version(self, runner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "konvert" in result.output
        assert "0.1.0" in result.output

    def test_help(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Universal data format converter" in result.output
        assert "Examples" in result.output


class TestErrors:
    def test_unsupported_format(self, runner, json_file):
        result = runner.invoke(main, [str(json_file), "xyz"])
        assert result.exit_code == 1
        assert "Unsupported" in result.output

    def test_no_target(self, runner, json_file):
        result = runner.invoke(main, [str(json_file)])
        assert result.exit_code != 0

    def test_file_not_found(self, runner):
        result = runner.invoke(main, ["/nonexistent.json", "yaml"])
        assert result.exit_code == 1
        assert "Error" in result.output


class TestBatch:
    def test_batch_conversion(self, runner, tmp_dir):
        (tmp_dir / "a.json").write_text('{"x": 1}', encoding="utf-8")
        (tmp_dir / "b.json").write_text('{"y": 2}', encoding="utf-8")
        result = runner.invoke(main, [str(tmp_dir), "--to", "yaml", "--batch"])
        assert result.exit_code == 0
        assert "2 file(s) converted" in result.output
        assert (tmp_dir / "a.yaml").exists()
        assert (tmp_dir / "b.yaml").exists()

    def test_batch_no_target(self, runner, tmp_dir):
        result = runner.invoke(main, [str(tmp_dir), "--batch"])
        assert result.exit_code == 1

    def test_batch_no_source(self, runner):
        result = runner.invoke(main, ["--batch", "--to", "yaml"])
        assert result.exit_code == 1


class TestInPlaceEdgeCases:
    def test_inplace_no_file(self, runner):
        result = runner.invoke(main, ["--to", "yaml", "--in-place"])
        assert result.exit_code == 1

    def test_inplace_no_format(self, runner, json_file):
        result = runner.invoke(main, [str(json_file), "--in-place"])
        assert result.exit_code == 1


class TestSchemaPipe:
    def test_schema_from_pipe(self, runner):
        result = runner.invoke(main, ["--schema"], input='{"a": 1}')
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert parsed["type"] == "object"
