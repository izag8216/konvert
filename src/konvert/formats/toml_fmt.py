"""TOML format handler."""

import tomlkit

from .base import BaseFormat


class TomlFormat(BaseFormat):
    """Handle TOML serialization and deserialization.

    Uses tomlkit to preserve comments and formatting.
    """

    def load(self, content: str) -> object:
        return tomlkit.loads(content)

    def to_plain(self, data: object) -> object:
        """Convert tomlkit objects to plain Python types for cross-format conversion."""
        if isinstance(data, dict):
            return {k: self.to_plain(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self.to_plain(item) for item in data]
        # tomlkit scalar types: use primitive constructors
        if hasattr(data, "unwrap"):
            return data.unwrap()
        if isinstance(data, bool):
            return bool(data)
        if isinstance(data, int):
            return int(data)
        if isinstance(data, float):
            return float(data)
        if isinstance(data, str):
            return str(data)
        return data

    def dump(self, data: object, pretty: bool = False) -> str:
        doc = tomlkit.document()
        if isinstance(data, dict):
            _build_toml_doc(doc, data)
        else:
            doc.add("value", data)
        return tomlkit.dumps(doc)


def _build_toml_doc(doc: tomlkit.TOMLDocument, data: dict) -> None:
    """Recursively build TOML document from dict, separating tables from inline values."""
    tables = {}
    for key, value in data.items():
        if isinstance(value, dict):
            tables[key] = value
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            tables[key] = value
        else:
            doc.add(key, value)
    for key, value in tables.items():
        if isinstance(value, list):
            for item in value:
                table = tomlkit.table()
                if isinstance(item, dict):
                    _build_toml_doc(table, item)
                doc.add(key, [table] if key not in doc else doc[key] + [table])
        else:
            table = tomlkit.table()
            _build_toml_doc(table, value)
            doc.add(key, table)
