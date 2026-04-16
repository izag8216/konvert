"""Tests for ENV format handler."""

import pytest

from konvert.formats.env_fmt import EnvFormat


@pytest.fixture
def handler():
    return EnvFormat()


class TestEnvLoad:
    def test_load_basic(self, handler, sample_env):
        result = handler.load(sample_env)
        assert result["NAME"] == "konvert"
        assert result["VERSION"] == "0.1.0"

    def test_load_skips_comments(self, handler):
        data = "# comment\nKEY=value\n"
        result = handler.load(data)
        assert result == {"KEY": "value"}

    def test_load_unquotes(self, handler):
        data = 'KEY="hello world"\n'
        result = handler.load(data)
        assert result["KEY"] == "hello world"

    def test_load_single_quotes(self, handler):
        data = "KEY='hello world'\n"
        result = handler.load(data)
        assert result["KEY"] == "hello world"


class TestEnvDump:
    def test_dump_basic(self, handler):
        data = {"KEY": "value", "PORT": "8080"}
        result = handler.dump(data)
        assert "KEY=value" in result
        assert "PORT=8080" in result

    def test_dump_quotes_spaces(self, handler):
        data = {"KEY": "hello world"}
        result = handler.dump(data)
        assert 'KEY="hello world"' in result

    def test_roundtrip(self, handler):
        data = {"NAME": "test", "PORT": "3000"}
        output = handler.dump(data)
        restored = handler.load(output)
        assert restored == data
