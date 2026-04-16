![header](https://capsule-render.vercel.app/api?type=flat&color=0D1117&fontColor=3FB950&font=FiraCode&height=120&text=konvert&desc=Universal%20Data%20Format%20Converter&section=header)

![Python](https://img.shields.io/badge/python-3.10%2B-3FB950?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-0D1117?style=flat)
![Tests](https://img.shields.io/badge/tests-116%20passing-3FB950?style=flat)
![Coverage](https://img.shields.io/badge/coverage-81%25-3FB950?style=flat)

[日本語](./README_ja.md)

# konvert

**Universal Data Format Converter CLI**

A zero-configuration, pipe-friendly command-line tool for converting between JSON, YAML, TOML, CSV, XML, INI, and .env file formats. Built with Python 3.10+ for simplicity and reliability.

## Features

- **Zero Configuration** -- just provide input and target format
- **7 Formats** -- JSON, YAML, TOML, CSV, XML, INI, .env (42 format pairs)
- **Auto-Detection** -- detects input format from file extension and content sniffing
- **Pipe-Friendly** -- read from stdin, write to stdout
- **Batch Mode** -- convert all matching files in a directory
- **In-Place** -- convert files without creating copies
- **Schema Detection** -- inspect data structure without converting
- **Comment Preservation** -- TOML comments survive round-trips via tomlkit

## Installation

```bash
git clone https://github.com/izag8216/konvert.git
cd konvert
pip install -e .
```

Requires Python 3.10+.

## Usage

### Basic Conversion

```bash
# JSON to YAML
konvert config.json yaml

# YAML to TOML
konvert settings.yaml toml

# JSON to XML
konvert data.json xml
```

### Pipe Mode

```bash
# stdin to stdout
cat config.json | konvert - yaml

# Chain with other tools
curl -s https://api.example.com/data | konvert - yaml
```

### With Flags

```bash
# Pretty-print output
konvert config.json yaml --pretty

# Specify input format explicitly
konvert data.yaml json -f yaml

# Write to file
konvert config.json yaml -o output.yaml
```

### In-Place Conversion

```bash
# Convert file, replacing original
konvert config.yaml --to json --in-place
# Creates config.json, removes config.yaml
```

### Batch Conversion

```bash
# Convert all files in a directory
konvert ./configs --to yaml --batch
```

### Schema Detection

```bash
konvert config.json --schema
```

Output:
```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "version": { "type": "string" }
  }
}
```

## Supported Formats

| Format | Extensions | Input | Output | Notes |
|--------|-----------|-------|--------|-------|
| JSON | `.json` | yes | yes | Full spec, nested structures |
| YAML | `.yaml`, `.yml` | yes | yes | PyYAML-based |
| TOML | `.toml` | yes | yes | Comment preservation via tomlkit |
| CSV | `.csv` | yes | yes | First row as headers |
| XML | `.xml` | yes | yes | Auto-wraps multi-key dicts |
| INI | `.ini`, `.cfg`, `.conf` | yes | yes | Section-based |
| .env | `.env` | yes | yes | KEY=VALUE format |

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v --cov=konvert
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Maintain 80%+ code coverage
6. Open a Pull Request

## License

MIT License -- see [LICENSE](./LICENSE) for details.

## Author

**izag8216** -- [GitHub](https://github.com/izag8216)
