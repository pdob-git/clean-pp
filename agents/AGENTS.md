# Agent Guidelines for clean-app

This is a Clean Architecture demo application with SQLite database and data export functionality.

## Project Structure

```
src/clean_app/
├── domain/                    # Business entities and interfaces
│   ├── entities/user.py      # User dataclass
│   └── repositories.py      # UserRepository abstract interface
├── application/              # Use cases (business logic)
│   ├── get_users.py         # GetUsersUseCase
│   └── export_data.py       # ExportDataUseCase
├── infrastructure/           # External adapters
│   ├── sqlite_repo.py       # SQLiteUserRepository implementation
│   └── exporters/           # Data exporters (OCP: add new without modifying)
│       ├── base.py          # DataExporter abstract base
│       ├── csv_exporter.py  # CSV exporter
│       └── excel_exporter.py
└── presentation/            # CLI interface
    └── cli.py               # Click-based CLI

tests/
├── test_application.py      # Use case tests (mock-based)
└── test_infrastructure.py   # Repository/exporter tests (integration)
```

## Commands

### Installation
```bash
pip install -e .              # Install package in editable mode
```

### Running the App
```bash
clean-app get-users --db-path users.db
clean-app export --db-path users.db --format csv --output output.csv
clean-app export --db-path users.db --format excel --output output.xlsx
```

### Linting & Type Checking
```bash
ruff check src/ tests/        # Lint all source files
mypy                          # Type check (uses pyproject.toml config)
ruff check src/ tests/ --fix  # Auto-fix lint issues
```

### Testing
```bash
pytest                        # Run all tests
pytest tests/                 # Same as above
pytest tests/ -v              # Verbose output
pytest tests/test_application.py -v              # Single test file
pytest tests/test_application.py::TestGetUsersUseCase::test_execute_returns_all_users -v  # Single test
pytest tests/test_infrastructure.py::TestCsvExporter::test_export_creates_file -v       # Single test
```

### Full Quality Check
```bash
ruff check src/ tests/ && mypy && pytest
```

## Code Style Guidelines

### Imports
- Use absolute imports: `from clean_app.domain.entities.user import User`
- Group imports: stdlib, third-party, local
- Sort alphabetically within groups
- Run `ruff check --fix` to auto-organize

### Formatting
- Line length: 100 characters max
- Use trailing newlines
- 4 spaces for indentation (no tabs)

### Type Hints
- Use Python 3.11+ union syntax: `User | None` (not `Optional[User]`)
- Add return types to all functions: `def foo() -> int:`
- Add parameter types: `def foo(x: int) -> str:`
- Use `list[User]` not `List[User]`

### Naming Conventions
- Classes: `PascalCase` (e.g., `SQLiteUserRepository`)
- Functions/variables: `snake_case` (e.g., `get_all_users`)
- Constants: `UPPER_SNAKE_CASE`
- Private methods: prefix with `_` (e.g., `_connect`)

### Data Classes
- Use `@dataclass` for simple data holders (entities)
- Define explicit types for all fields

### SOLID Principles
- **SRP**: Each module has one responsibility
- **OCP**: Use abstract interfaces; extend by adding new classes, not modifying existing
- **DIP**: Application layer depends on domain abstractions, not concrete implementations

### Error Handling
- Raise descriptive exceptions: `raise ValueError(f"Unsupported format: {format_type}")`
- Don't catch generic `Exception` unless necessary
- Let errors propagate to presentation layer

### Clean Architecture Layers
- **Domain**: Entities, repository interfaces (no external dependencies)
- **Application**: Use cases, business logic (depends only on domain)
- **Infrastructure**: Repository implementations, exporters (implements domain interfaces)
- **Presentation**: CLI, user interaction (orchestrates layers)

### Testing
- Unit tests: Use mocks for dependencies
- Integration tests: Test with real SQLite/exporter
- Test file naming: `test_<module>.py`
- Test class naming: `Test<ClassName>`
- Test method naming: `test_<behavior>`

### Adding New Exporters
1. Create new class implementing `DataExporter` in `infrastructure/exporters/`
2. Add to `EXPORTERS` dict in `infrastructure/exporters/__init__.py`
3. No changes to existing code required (OCP)

## Dependencies
- click>=8.0 (CLI)
- pandas>=2.0 (Excel export)
- openpyxl>=3.0 (Excel format)
- pytest>=8.0 (testing)
- ruff (linting)
- mypy (type checking)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                       │
│                         (presentation/cli.py)                    │
│                              CLI commands                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Application Layer                          │
│           (application/get_users.py, export_data.py)           │
│                          Use Cases                               │
│    GetUsersUseCase  ──────►  ExportDataUseCase                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Domain Layer                            │
│           (domain/entities/user.py, repositories.py)             │
│                    Entities & Interfaces                         │
│              User          UserRepository (ABC)                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │ implements
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Infrastructure Layer                        │
│         (infrastructure/sqlite_repo.py, exporters/)             │
│                    Concrete Implementations                     │
│    SQLiteUserRepository  ──►  DataExporter (ABC)               │
│                           CsvExporter, ExcelExporter            │
└─────────────────────────────────────────────────────────────────┘
```

## Dependency Rule
Dependencies flow inward: Presentation → Application → Domain ← Infrastructure

Inner layers know nothing about outer layers. Use dependency injection.

## Database Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    loginname TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL
);
```

## Common Tasks

### Adding a New Database
1. Implement `UserRepository` interface in `infrastructure/`
2. Inject into use cases via presentation layer

### Adding a New Export Format
1. Create class implementing `DataExporter` in `infrastructure/exporters/`
2. Add to `EXPORTERS` dict in `infrastructure/exporters/__init__.py`

### Running a Specific Test
```bash
pytest tests/test_application.py::TestGetUsersUseCase::test_execute_returns_all_users -v
```

### Debugging
- Use `python -c "from clean_app import *"` to test imports
- Add `import pdb; pdb.set_trace()` for debugging
- Check logs in CLI output for errors