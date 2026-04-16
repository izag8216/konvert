"""Tests for CSV format handler."""

import pytest

from konvert.formats.csv_fmt import CsvFormat


@pytest.fixture
def handler():
    return CsvFormat()


class TestCsvLoad:
    def test_load_basic(self, handler, sample_csv):
        result = handler.load(sample_csv)
        assert len(result) == 2
        assert result[0]["name"] == "konvert"
        assert result[0]["version"] == "0.1.0"

    def test_load_single_column(self, handler):
        data = "name\nalice\nbob\n"
        result = handler.load(data)
        assert result == [{"name": "alice"}, {"name": "bob"}]


class TestCsvDump:
    def test_dump_list_of_dicts(self, handler):
        data = [{"name": "alice", "age": "30"}, {"name": "bob", "age": "25"}]
        result = handler.dump(data)
        assert "name,age" in result
        assert "alice,30" in result

    def test_dump_single_dict(self, handler):
        data = {"name": "test"}
        result = handler.dump(data)
        assert "name" in result
        assert "test" in result

    def test_dump_empty_list(self, handler):
        result = handler.dump([])
        assert result == ""

    def test_roundtrip(self, handler, sample_csv):
        data = handler.load(sample_csv)
        output = handler.dump(data)
        restored = handler.load(output)
        assert restored == data
