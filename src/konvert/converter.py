"""Core conversion engine."""

from pathlib import Path

from .detector import detect_from_content, detect_from_extension, detect_schema
from .formats import FORMATS


class ConverterError(Exception):
    """Conversion error."""


def convert(
    source: str | None = None,
    target_format: str | None = None,
    input_format: str | None = None,
    pretty: bool = False,
    content: str | None = None,
) -> str:
    """Convert data from one format to another.

    Args:
        source: Input file path (optional, stdin used if None).
        target_format: Target format name.
        input_format: Input format override (auto-detected if None).
        pretty: Pretty-print output.
        content: Direct content string (used when reading from stdin).

    Returns:
        Converted string.
    """
    if target_format is None:
        raise ConverterError("Target format is required")

    target_format = target_format.lower()

    if target_format not in FORMATS:
        raise ConverterError(f"Unsupported target format: {target_format}")

    # Read input
    if content is not None:
        raw = content
        if input_format is None:
            input_format = detect_from_content(raw)
    elif source is not None:
        path = Path(source)
        if not path.exists():
            raise ConverterError(f"File not found: {source}")
        raw = path.read_text(encoding="utf-8")
        if input_format is None:
            input_format = detect_from_extension(source)
            if input_format is None:
                input_format = detect_from_content(raw)
    else:
        raise ConverterError("No input source provided")

    if input_format is None:
        raise ConverterError("Could not detect input format")

    input_format = input_format.lower()
    if input_format not in FORMATS:
        raise ConverterError(f"Unsupported input format: {input_format}")

    # Load -> dump
    source_handler = FORMATS[input_format]()
    target_handler = FORMATS[target_format]()

    data = source_handler.load(raw)

    # Normalize tomlkit objects to plain dicts for cross-format compatibility
    if hasattr(source_handler, "to_plain"):
        data = source_handler.to_plain(data)

    return target_handler.dump(data, pretty=pretty)


def detect_input_schema(
    source: str | None = None,
    input_format: str | None = None,
    content: str | None = None,
) -> dict:
    """Detect and return the schema of input data."""
    if content is not None:
        raw = content
        if input_format is None:
            input_format = detect_from_content(raw)
    elif source is not None:
        path = Path(source)
        if not path.exists():
            raise ConverterError(f"File not found: {source}")
        raw = path.read_text(encoding="utf-8")
        if input_format is None:
            input_format = detect_from_extension(source)
            if input_format is None:
                input_format = detect_from_content(raw)
    else:
        raise ConverterError("No input source provided")

    if input_format is None:
        raise ConverterError("Could not detect input format")

    input_format = input_format.lower()
    if input_format not in FORMATS:
        raise ConverterError(f"Unsupported input format: {input_format}")

    handler = FORMATS[input_format]()
    data = handler.load(raw)
    return detect_schema(data)
