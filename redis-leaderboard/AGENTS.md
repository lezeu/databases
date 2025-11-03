# AGENTS.md

## Build/Lint/Test Commands
- **Test single file**: `python -m pytest Redis/test_file.py -v`
- **Test all**: `python -m pytest` (if pytest configured)
- **Lint**: `python -m flake8 Redis/` (if flake8 configured)
- **Format**: `python -m black Redis/` (if black configured)
- **Type check**: `python -m mypy Redis/` (if mypy configured)

## Code Style Guidelines

### Imports
- Standard library imports first
- Third-party imports second
- Local imports last
- Use `import module` for stdlib/third-party, `from module import item` for local

### Naming
- `snake_case` for variables, functions, methods
- `UPPER_CASE` for constants
- `CamelCase` for classes (if any)

### Formatting
- Use f-strings for string formatting
- 4 spaces for indentation
- Line length: 88 characters (Black default)

### Types
- Add type hints for function parameters and return values when beneficial
- Use `typing` module imports as needed

### Error Handling
- Use try/except blocks for Redis operations
- Log errors appropriately
- Handle connection failures gracefully

### Comments
- Use `#` for inline comments
- Use `##` for section headers
- Keep comments concise and meaningful