"""XML format handler."""

import xmltodict

from .base import BaseFormat


class XmlFormat(BaseFormat):
    """Handle XML serialization and deserialization."""

    def load(self, content: str) -> dict:
        return xmltodict.parse(content)

    def dump(self, data: object, pretty: bool = False) -> str:
        if not isinstance(data, dict):
            data = {"value": data}
        # Ensure single root element
        if len(data) != 1:
            data = {"root": data}
        return xmltodict.unparse(data, pretty=pretty)
