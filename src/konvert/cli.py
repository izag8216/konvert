"""CLI entry point for konvert."""

import json
import sys
from pathlib import Path

import click

from . import __version__
from .converter import ConverterError, convert, detect_input_schema
from .formats import FORMATS

SUPPORTED_FORMATS = sorted(set(FORMATS.keys()) - {"yml"})


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("source", required=False)
@click.argument("target_format", required=False)
@click.option("-f", "--from", "input_format", help="Input format (auto-detected by default)")
@click.option("-t", "--to", "to_format", help="Target format (alternative to positional arg)")
@click.option("--in-place", is_flag=True, help="Convert file in-place")
@click.option("--batch", is_flag=True, help="Convert all matching files in directory")
@click.option("--pretty", is_flag=True, help="Pretty-print output")
@click.option("--schema", is_flag=True, help="Show detected schema without converting")
@click.option("-o", "--output", help="Output file path (default: stdout)")
@click.version_option(version=__version__, prog_name="konvert")
def main(
    source: str | None,
    target_format: str | None,
    input_format: str | None,
    to_format: str | None,
    in_place: bool,
    batch: bool,
    pretty: bool,
    schema: bool,
    output: str | None,
) -> None:
    """konvert - Universal data format converter.

    Convert between JSON, YAML, TOML, CSV, XML, INI, and .env formats.

    \b
    Examples:
        konvert data.json yaml              # Convert file
        konvert data.json --schema          # Show schema
        cat data.json | konvert - yaml      # Pipe mode
        konvert config.yaml --to json       # Using --to flag
        konvert *.csv --to json --batch     # Batch conversion
    """
    # Resolve target format
    fmt = to_format or target_format
    if fmt == "-":
        fmt = None

    # Schema detection mode
    if schema:
        _handle_schema(source, input_format)
        return

    # Validate target format
    if fmt and fmt.lower() not in FORMATS:
        click.echo(f"Error: Unsupported format '{fmt}'. Supported: {', '.join(SUPPORTED_FORMATS)}", err=True)
        sys.exit(1)

    # Batch mode
    if batch:
        _handle_batch(source, fmt, input_format, pretty)
        return

    # In-place mode
    if in_place:
        _handle_inplace(source, fmt, input_format)
        return

    # Single conversion
    _handle_single(source, fmt, input_format, pretty, output)


def _handle_schema(source: str | None, input_format: str | None) -> None:
    """Handle --schema mode."""
    if source and source != "-":
        content = None
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
        source = None
    else:
        click.echo("Error: No input source for schema detection", err=True)
        sys.exit(1)

    try:
        result = detect_input_schema(source=source, input_format=input_format, content=content)
        click.echo(json.dumps(result, indent=2))
    except ConverterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def _handle_single(
    source: str | None,
    target_format: str | None,
    input_format: str | None,
    pretty: bool,
    output: str | None,
) -> None:
    """Handle single file/stdin conversion."""
    content = None
    if source == "-" or (source is None and not sys.stdin.isatty()):
        content = sys.stdin.read()
        source = None

    if target_format is None:
        click.echo("Error: Target format required. Usage: konvert <source> <format>", err=True)
        sys.exit(1)

    try:
        result = convert(
            source=source,
            target_format=target_format,
            input_format=input_format,
            pretty=pretty,
            content=content,
        )
    except ConverterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if output:
        Path(output).write_text(result, encoding="utf-8")
    else:
        click.echo(result, nl=False)


def _handle_inplace(
    source: str | None,
    target_format: str | None,
    input_format: str | None,
) -> None:
    """Handle --in-place conversion."""
    if source is None or source == "-":
        click.echo("Error: --in-place requires a file path", err=True)
        sys.exit(1)

    if target_format is None:
        click.echo("Error: --in-place requires --to format", err=True)
        sys.exit(1)

    path = Path(source)
    ext_map = {
        "json": ".json",
        "yaml": ".yaml",
        "toml": ".toml",
        "csv": ".csv",
        "xml": ".xml",
        "ini": ".ini",
        "env": ".env",
    }
    new_ext = ext_map.get(target_format.lower(), f".{target_format.lower()}")
    new_path = path.with_suffix(new_ext)

    try:
        result = convert(source=source, target_format=target_format, input_format=input_format)
    except ConverterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    new_path.write_text(result, encoding="utf-8")
    if new_path != path:
        path.unlink()
    click.echo(f"Converted: {path} -> {new_path}")


def _handle_batch(
    source: str | None,
    target_format: str | None,
    input_format: str | None,
    pretty: bool,
) -> None:
    """Handle --batch conversion."""
    if target_format is None:
        click.echo("Error: --batch requires --to format", err=True)
        sys.exit(1)

    if source is None:
        click.echo("Error: --batch requires a file pattern or directory", err=True)
        sys.exit(1)

    src = Path(source)
    if src.is_dir():
        files = list(src.iterdir())
    else:
        parent = src.parent
        pattern = src.name
        files = list(parent.glob(pattern))

    if not files:
        click.echo(f"No files found matching: {source}", err=True)
        sys.exit(1)

    ext_map = {
        "json": ".json",
        "yaml": ".yaml",
        "toml": ".toml",
        "csv": ".csv",
        "xml": ".xml",
        "ini": ".ini",
        "env": ".env",
    }
    new_ext = ext_map.get(target_format.lower(), f".{target_format.lower()}")
    converted = 0

    for f in files:
        if f.is_dir():
            continue
        try:
            result = convert(source=str(f), target_format=target_format, input_format=input_format, pretty=pretty)
            out_path = f.with_suffix(new_ext)
            out_path.write_text(result, encoding="utf-8")
            click.echo(f"Converted: {f.name} -> {out_path.name}")
            converted += 1
        except ConverterError as e:
            click.echo(f"Skipped {f.name}: {e}", err=True)

    click.echo(f"\nBatch complete: {converted} file(s) converted")
