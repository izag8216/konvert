"""JSON format handler."""

import json

from .base import BaseFormat


class JsonFormat(BaseFormat):
    """Handle JSON serialization and deserialization."""

    def load(self, content: str) -> object:
        return json.loads(content)

    def dump(self, data: object, pretty: bool = False) -> str:
        if pretty:
            return json.dumps(data, indent=2, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)
