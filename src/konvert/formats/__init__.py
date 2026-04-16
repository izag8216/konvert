"""Format handler registry."""

from .json_fmt import JsonFormat
from .yaml_fmt import YamlFormat
from .toml_fmt import TomlFormat
from .csv_fmt import CsvFormat
from .xml_fmt import XmlFormat
from .ini_fmt import IniFormat
from .env_fmt import EnvFormat

FORMATS: dict[str, type] = {
    "json": JsonFormat,
    "yaml": YamlFormat,
    "yml": YamlFormat,
    "toml": TomlFormat,
    "csv": CsvFormat,
    "xml": XmlFormat,
    "ini": IniFormat,
    "env": EnvFormat,
}

FORMAT_ALIASES: dict[str, str] = {
    "yml": "yaml",
}

__all__ = [
    "FORMATS",
    "FORMAT_ALIASES",
    "JsonFormat",
    "YamlFormat",
    "TomlFormat",
    "CsvFormat",
    "XmlFormat",
    "IniFormat",
    "EnvFormat",
]
