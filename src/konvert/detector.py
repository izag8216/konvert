"""Format auto-detection from file extension and content."""

from pathlib import Path

EXTENSION_MAP: dict[str, str] = {
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".csv": "csv",
    ".xml": "xml",
    ".ini": "ini",
    ".cfg": "ini",
    ".conf": "ini",
    ".env": "env",
}


def detect_from_extension(filepath: str) -> str | None:
    """Detect format from file extension or filename."""
    p = Path(filepath)
    name = p.name.lower()
    if name == ".env" or name.endswith(".env"):
        return "env"
    ext = p.suffix.lower()
    return EXTENSION_MAP.get(ext)


def detect_from_content(content: str) -> str | None:
    """Detect format by sniffing content.

    Tries parsing heuristics in order of specificity.
    """
    stripped = content.strip()
    if not stripped:
        return None

    # JSON object: starts with {
    if stripped.startswith("{"):
        return "json"

    # XML: starts with < (possibly with <?xml declaration)
    if stripped.startswith("<"):
        return "xml"

    # Distinguish [section] (TOML/INI) from JSON arrays [1, 2, 3]
    if stripped.startswith("["):
        # JSON array: next char after [ is digit, ", [, {, true/false/null, or ]
        after_bracket = stripped[1:].lstrip()
        if after_bracket and after_bracket[0] in {'"', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '[', '{', ']'}:
            return "json"
        if after_bracket.startswith(("true", "false", "null")):
            return "json"

    # TOML: has [section] headers with key = "quoted" values, or dotted keys
    # INI: has [section] headers with key = unquoted values
    if _looks_like_toml(stripped):
        return "toml"

    # INI: has [section] headers (check after TOML since TOML is stricter)
    if _looks_like_ini(stripped):
        return "ini"

    # ENV: KEY=VALUE pattern (no sections)
    if _looks_like_env(stripped):
        return "env"

    # INI: has [section] headers
    if _looks_like_ini(stripped):
        return "ini"

    # CSV: comma-separated lines with consistent columns
    if _looks_like_csv(stripped):
        return "csv"

    # YAML: fallback (most flexible format)
    if _looks_like_yaml(stripped):
        return "yaml"

    return None


def _looks_like_toml(content: str) -> bool:
    """Check if content looks like TOML (stricter than INI)."""
    lines = content.splitlines()
    has_header = False
    has_quoted_value = False
    has_kv = False
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("[") and not s.startswith("[["):
            has_header = True
        if "=" in s and not s.startswith("["):
            has_kv = True
            # TOML values are often quoted strings or typed
            value_part = s.split("=", 1)[1].strip()
            if value_part.startswith('"') or value_part.startswith("'"):
                has_quoted_value = True
    # TOML needs section headers; prefer quoted values to distinguish from INI
    return has_header and has_kv and has_quoted_value


def _looks_like_env(content: str) -> bool:
    """Check if content looks like .env format."""
    lines = content.splitlines()
    env_count = 0
    total = 0
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        total += 1
        if "=" in s:
            key = s.split("=")[0].strip()
            if key.isidentifier() or all(c.isalnum() or c == "_" for c in key):
                env_count += 1
    return total > 0 and env_count == total


def _looks_like_ini(content: str) -> bool:
    """Check if content looks like INI format."""
    lines = content.splitlines()
    for line in lines:
        s = line.strip()
        if s.startswith("[") and s.endswith("]") and not s.startswith("[["):
            return True
    return False


def _looks_like_csv(content: str) -> bool:
    """Check if content looks like CSV."""
    lines = content.splitlines()
    if len(lines) < 2:
        return False
    first_commas = lines[0].count(",")
    if first_commas == 0:
        return False
    return all(line.count(",") == first_commas for line in lines[:3])


def _looks_like_yaml(content: str) -> bool:
    """Check if content looks like YAML (has key: value patterns)."""
    lines = content.splitlines()
    for line in lines:
        s = line.strip()
        if ": " in s or s.endswith(":"):
            return True
    return False


def detect_schema(data: object, _depth: int = 0) -> dict:
    """Analyze data structure and return schema description."""
    if _depth > 10:
        return {"type": "unknown"}

    if data is None:
        return {"type": "null"}
    if isinstance(data, bool):
        return {"type": "boolean"}
    if isinstance(data, int):
        return {"type": "integer"}
    if isinstance(data, float):
        return {"type": "float"}
    if isinstance(data, str):
        return {"type": "string"}

    if isinstance(data, list):
        if not data:
            return {"type": "array", "items": "empty"}
        sample = data[0]
        return {
            "type": "array",
            "length": len(data),
            "items": detect_schema(sample, _depth + 1),
        }

    if isinstance(data, dict):
        properties = {}
        for key, value in data.items():
            properties[key] = detect_schema(value, _depth + 1)
        return {"type": "object", "properties": properties}

    return {"type": type(data).__name__}
