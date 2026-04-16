# Contributing to konvert

Thank you for your interest in contributing to konvert! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- GitHub account

### Development Setup

1. **Fork the repository**

   Click the "Fork" button in the top-right corner of the repository page.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/konvert.git
   cd konvert
   ```

3. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install development dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

5. **Run tests**

   ```bash
   pytest tests/ -v
   ```

## Development Workflow

1. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**

   - Write code following the existing style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests**

   ```bash
   pytest tests/ -v --cov=konvert
   ```

   Ensure all tests pass and coverage is maintained at 80% or higher.

4. **Commit your changes**

   Use [Conventional Commits](https://www.conventionalcommits.org/):

   ```
   feat: add support for converting from environment variables
   fix: handle empty CSV files correctly
   docs: update installation instructions
   test: add tests for XML conversion edge cases
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

   - Visit the original repository on GitHub
   - Click "Compare & pull request"
   - Fill out the PR template
   - Link any related issues

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write descriptive docstrings for functions and classes
- Keep functions focused and concise

## Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use pytest for testing
- Include tests for edge cases and error conditions

## Documentation

- Update relevant documentation when adding features
- Keep examples in `examples/` up to date
- Update CHANGELOG.md for user-facing changes

## License

By contributing to konvert, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions about contributing!
