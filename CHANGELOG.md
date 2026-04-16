# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-16

### Added
- Initial release
- Convert between JSON, YAML, TOML, CSV, XML, INI, .env formats
- Auto-detect format from file extension and content
- Pipe-friendly stdin/stdout support
- In-place conversion (--in-place)
- Batch conversion (--batch)
- Schema detection (--schema)
- Pretty-print output (--pretty)
- Comment preservation for TOML via tomlkit
