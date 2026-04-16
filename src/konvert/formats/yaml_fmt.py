"""YAML format handler."""

import yaml

from .base import BaseFormat


class YamlFormat(BaseFormat):
    """Handle YAML serialization and deserialization."""

    def load(self, content: str) -> object:
        result = yaml.safe_load(content)
        return result if result is not None else {}

    def dump(self, data: object, pretty: bool = False) -> str:
        result = yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=not pretty,
        )
        return result
