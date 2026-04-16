# Supported Formats

konvert supports the following data formats:

| Format | Extensions | Read Support | Write Support | Notes |
|--------|-----------|--------------|---------------|-------|
| **JSON** | `.json` | ✅ Yes | ✅ Yes | Most widely supported format. Preserves data types (strings, numbers, booleans, null). |
| **YAML** | `.yaml`, `.yml` | ✅ Yes | ✅ Yes | Human-readable format. Supports anchors, aliases, and complex data structures. |
| **TOML** | `.toml` | ✅ Yes | ✅ Yes | Configuration file format. **Comments are preserved during conversion** using tomlkit. |
| **CSV** | `.csv` | ✅ Yes | ✅ Yes | Comma-separated values. First row is used as headers. Converts to/from nested dictionaries. |
| **XML** | `.xml` | ✅ Yes | ✅ Yes | Markup language. Attributes and text content are preserved in dictionary representation. |
| **INI** | `.ini`, `.cfg`, `.conf` | ✅ Yes | ✅ Yes | Configuration files with sections. Nested structure preserved. |
| **ENV** | `.env` | ✅ Yes | ✅ Yes | Environment variable files. Simple key=value pairs. Values are always strings. |

## Format-Specific Behavior

### JSON
- Preserves numeric types (integers and floats)
- Distinguishes between `null`, `true`, `false`
- Output is minified by default; use `--pretty` for formatted output

### YAML
- Supports all YAML 1.2 features
- Preserves multi-line strings and complex types
- Output is formatted by default

### TOML
- **Comments are preserved** when reading and writing TOML files
- Uses `tomlkit` library for comment preservation
- Best suited for configuration files

### CSV
- First row is used as column headers
- Converts to flat dictionary structure
- Nested data structures are flattened with dot notation (e.g., `config.verbose`)

### XML
- Attributes become prefixed with `@` (e.g., `@id`)
- Text content is stored under `#text` key
- Nested elements become nested dictionaries
- Multiple elements with same name become lists

### INI
- Sections become top-level keys
- Key-value pairs within sections become nested dictionaries
- Comments are NOT preserved

### ENV
- All values are strings
- Lines starting with `#` are treated as comments (ignored during parsing)
- Empty lines are skipped
- No nested structure support

## Auto-Detection

konvert automatically detects input format from:
1. File extension (primary)
2. File content (secondary, for files without extension)

Output format is determined by:
1. Output file extension (if specified)
2. Explicit `--output-format` flag

## Conversion Matrix

All formats can be converted to/from each other with the following considerations:

- **CSV** → **JSON/YAML/TOML/XML/INI**: Works seamlessly. Each row becomes a dictionary entry.
- **JSON/YAML/TOML/XML/INI** → **CSV**: Nested structures are flattened using dot notation.
- **ENV** → **Other formats**: All values are strings. May need type conversion.
- **Other formats** → **ENV**: Nested structures are flattened. Complex types (lists, dicts) are stringified.
