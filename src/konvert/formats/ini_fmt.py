"""INI format handler."""

import configparser
import io

from .base import BaseFormat


class IniFormat(BaseFormat):
    """Handle INI serialization and deserialization."""

    def load(self, content: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read_string(content)
        result: dict = {}
        for section in parser.sections():
            result[section] = dict(parser[section])
        return result

    def dump(self, data: object, pretty: bool = False) -> str:
        parser = configparser.ConfigParser()
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    parser[key] = {k: str(v) for k, v in value.items()}
                else:
                    if "DEFAULT" not in parser:
                        pass
                    parser.setdefault("DEFAULT", {})[key] = str(value)
        output = io.StringIO()
        parser.write(output)
        return output.getvalue()
