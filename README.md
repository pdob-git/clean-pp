# Clean App

A Clean Architecture demo application with SQLite database and data export functionality.

## Overview

This is a demonstration project showcasing Clean Architecture principles with SOLID design patterns. The application allows users to retrieve data from a SQLite database and export it to CSV or Excel formats.

## Features

- Get users from SQLite database
- Export user data to CSV or Excel format
- CLI-based interface using Click
- Clean Architecture with clear separation of concerns

## Architecture

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
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Domain Layer                            │
│           (domain/entities/user.py, repositories.py)             │
│                    Entities & Interfaces                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │ implements
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Infrastructure Layer                        │
│         (infrastructure/sqlite_repo.py, exporters/)             │
│                    Concrete Implementations                     │
└─────────────────────────────────────────────────────────────────┘
```

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

## Prerequisites

- Python 3.11+
- SQLite3

## Installation

```bash
pip install -e .
```

## Usage

### Initialize Database

```bash
python scripts/init_db.py
```

This creates a sample database with 5 users for testing.

### Get Users

```bash
clean-app get-users --db-path users.db
```

### Export Data

Export to CSV:
```bash
clean-app export --db-path users.db --format csv --output output.csv
```

Export to Excel:
```bash
clean-app export --db-path users.db --format excel --output output.xlsx
```

### Login (Demo)

```bash
clean-app login --host localhost --user admin --password secret --db-path users.db
```

Note: This is a demo command that stores credentials but doesn't validate them.

## Development

### Install Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Run Linting

```bash
ruff check src/ tests/
```

### Run Type Checking

```bash
mypy
```

### Full Quality Check

```bash
ruff check src/ tests/ && mypy && pytest
```

## SOLID Principles

| Principle | Implementation |
|-----------|----------------|
| **SRP** | Each module has one responsibility |
| **OCP** | Use abstract interfaces; extend by adding new classes |
| **LSP** | `SQLiteUserRepository` substitutable for `UserRepository` |
| **ISP** | `DataExporter` interface with single `export()` method |
| **DIP** | Application layer depends on domain abstractions |

## Adding New Export Formats

1. Create a new class implementing `DataExporter` in `infrastructure/exporters/`
2. Add to `EXPORTERS` dict in `infrastructure/exporters/__init__.py`

No changes to existing code required (Open/Closed Principle).

## License

MIT
