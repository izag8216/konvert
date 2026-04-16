# Basic Usage Examples

This document provides practical examples of using konvert in various scenarios.

## Installation

```bash
pip install konvert
```

## Examples

### 1. Basic Conversion (JSON to YAML)

Convert a JSON file to YAML:

```bash
konvert sample.json output.yaml
```

The output file will contain:
```yaml
name: konvert
version: 0.1.0
description: Universal data format converter
```

### 2. Pipe Mode (stdin/stdout)

Convert data from stdin:

```bash
cat config.json | konvert --from json --to yaml > config.yaml
```

Or with heredocs:
```bash
konvert --from json --to yaml << EOF
{
  "app": "myapp",
  "port": 8080
}
EOF
```

### 3. Auto-Detect Format

konvert automatically detects format from file extensions:

```bash
# Explicitly
konvert data.json output.toml

# Auto-detected (both from and to)
konvert config.yaml data.json
```

### 4. Pretty Print Output

Format output for readability:

```bash
konvert input.json output.yaml --pretty
```

This produces nicely formatted YAML with proper indentation.

### 5. Schema Detection

Detect and display the structure of your data:

```bash
konvert sample.json --schema
```

Output:
```
Schema:
  name: str
  version: str
  description: str
  features: List[str]
  config: Dict
    pretty: bool
    verbose: bool
```

### 6. In-Place Conversion

Convert and replace the original file:

```bash
konvert config.yaml --in-place --output-format json
```

The file `config.yaml` will be replaced with `config.json` containing the converted data.

### 7. Batch Conversion

Convert multiple files at once:

```bash
konvert --batch --output-format yaml *.json
```

This converts all `.json` files in the current directory to `.yaml` files.

### 8. All Supported Formats

Convert between any of the 7 supported formats:

```bash
# JSON to TOML
konvert config.json output.toml

# YAML to XML
konvert data.yaml output.xml

# TOML to INI
konvert config.toml output.ini

# CSV to JSON
konvert data.csv output.json

# XML to YAML
konvert data.xml output.yaml

# INI to ENV
konvert config.ini output.env

# ENV to TOML
konvert .env config.toml
```

### 9. Conversion with Comments Preserved (TOML)

When working with TOML files, comments are preserved:

**Input (config.toml):**
```toml
# Server configuration
port = 8080  # Default port
host = "localhost"
```

```bash
konvert config.toml temp.yaml --in-place
konvert temp.yaml config.toml --in-place
```

**Output (config.toml):**
```toml
# Server configuration
port = 8080  # Default port
host = "localhost"
```

### 10. Combining with Other Tools

Use konvert in shell pipelines:

```bash
# Fetch JSON from API and convert to YAML
curl -s https://api.example.com/config | konvert --from json --to yaml > config.yaml

# Convert CSV to JSON and process with jq
konvert data.csv --from csv --to json | jq '.[] | select(.age > 30)'

# Convert multiple files and archive
konvert --batch --output-format yaml *.json && tar czf yaml-configs.tar.gz *.yaml
```

## Tips

- Use `--help` to see all available options
- Combine `--pretty` with `--output-format` for formatted output to stdout
- Use `--in-place` with caution: it overwrites the original file
- For CSV files, ensure the first row contains headers
- TOML comments are only preserved when both input and output are TOML format
