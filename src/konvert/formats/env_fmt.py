"""ENV (.env) format handler."""

from .base import BaseFormat


class EnvFormat(BaseFormat):
    """Handle .env file serialization and deserialization."""

    def load(self, content: str) -> dict:
        result = {}
        for line in content.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            result[key] = value
        return result

    def dump(self, data: object, pretty: bool = False) -> str:
        if not isinstance(data, dict):
            return f"VALUE={data}\n"
        lines = []
        for key, value in data.items():
            if isinstance(value, str) and (" " in value or '"' in value or "'" in value):
                lines.append(f'{key}="{value}"')
            else:
                lines.append(f"{key}={value}")
        return "\n".join(lines) + "\n"
