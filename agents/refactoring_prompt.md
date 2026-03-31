# Refactoring Clean architecture

--- 
now i have starting point of program in presentation/cli.py but it violates rule that cannot import from infrastructure
architecture tests errors:

```commandline
pytest tests/test_architecture.py                                                                                                                                                               ─╯
======================================================================================== test session starts =========================================================================================
platform linux -- Python 3.12.9, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/synkmint/Gitrepos/Python/opencode/clean-app
configfile: pyproject.toml
plugins: archon-0.0.7
collected 1 item                                                                                                                                                                                     

tests/test_architecture.py F                                                                                                                                                                   [100%]

============================================================================================== FAILURES ==============================================================================================
_________________________________________________________________________________ test_clean_architecture_compliance _________________________________________________________________________________
FAILED Rule 'Application isolation':
- module 'clean_app.application.export_data' has FORBIDDEN import clean_app.infrastructure.exporters.base (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.application.export_data ↣ clean_app.infrastructure.exporters.base
FAILED Rule 'Presentation isolation':
- module 'clean_app.presentation.cli' has FORBIDDEN import clean_app.infrastructure.exporters.base (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.presentation.cli ↣ clean_app.application.export_data ↣ clean_app.infrastructure.exporters.base
- module 'clean_app.presentation.cli' has FORBIDDEN import clean_app.infrastructure.exporters (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.presentation.cli ↣ clean_app.infrastructure.exporters
- module 'clean_app.presentation.cli' has FORBIDDEN import clean_app.infrastructure.exporters.excel_exporter (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.presentation.cli ↣ clean_app.infrastructure.exporters ↣ clean_app.infrastructure.exporters.excel_exporter
- module 'clean_app.presentation.cli' has FORBIDDEN import clean_app.infrastructure.exporters.base (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.presentation.cli ↣ clean_app.infrastructure.exporters ↣ clean_app.infrastructure.exporters.excel_exporter ↣ clean_app.infrastructure.exporters.base
- module 'clean_app.presentation.cli' has FORBIDDEN import clean_app.infrastructure.exporters.csv_exporter (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.presentation.cli ↣ clean_app.infrastructure.exporters ↣ clean_app.infrastructure.exporters.csv_exporter
- module 'clean_app.presentation.cli' has FORBIDDEN import clean_app.infrastructure.exporters.base (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.presentation.cli ↣ clean_app.infrastructure.exporters ↣ clean_app.infrastructure.exporters.base
    from clean_app.presentation.cli ↣ clean_app.infrastructure.exporters ↣ clean_app.infrastructure.exporters.csv_exporter ↣ clean_app.infrastructure.exporters.base
- module 'clean_app.presentation.cli' has FORBIDDEN import clean_app.infrastructure.sqlite_repo (matched by glob pattern /clean_app.infrastructure*/)
    from clean_app.presentation.cli ↣ clean_app.infrastructure.sqlite_repo
====================================================================================== short test summary info =======================================================================================
FAILED tests/test_architecture.py::test_clean_architecture_compliance - FAILED Rule 'Application isolation':
========================================================================================= 1 failed in 0.05s ==========================================================================================

```

---

This is a **very common confusion** when implementing Clean Architecture in Python CLI apps — and you’re actually very close to the correct solution. 👍

Your situation:

```
presentation/cli.py  ← entrypoint
```

And you’re worried because:

```
presentation → infrastructure   ❌ forbidden
```

But your CLI must somehow **wire dependencies** (e.g., create DB repo, email client, etc.), which *are* infrastructure objects.

This is where **composition root** comes in.

---

# 🧠 Key principle: **The entrypoint is allowed to break the rule**

The Clean Architecture rule:

> Dependencies must point inward

applies to **application code**, not to the **startup script**.

The entrypoint is:

```
main.py
cli.py
app.py
```

and it is considered:

```
Frameworks & Drivers layer
```

which is **outside the architecture rings**.

So this is **allowed**:

```
cli.py → infrastructure → application → domain
```

because the entrypoint is not part of the “presentation layer” in the architectural sense — it is **bootstrap code**.

---

# Correct structure for a CLI Clean Architecture project

Recommended:

```
src/
├── domain/
├── application/
├── presentation/
│   └── cli_commands.py      # command handlers only
├── infrastructure/
└── main.py                  # composition root
```

### `main.py` responsibilities:

* create infrastructure objects
* wire them into use cases
* call presentation layer

---

# Example of correct dependency flow

### main.py (composition root)

```python
from infrastructure.db import SqlUserRepository
from infrastructure.email import SmtpEmailSender

from application.usecases.register_user import RegisterUser
from presentation.cli_commands import register_user_command


def main():
    repo = SqlUserRepository()
    email = SmtpEmailSender()

    use_case = RegisterUser(repo, email)

    register_user_command(use_case)


if __name__ == "__main__":
    main()
```

This file is **allowed** to import everything because:

```
it is not part of the architecture layers
```

---

# presentation/cli_commands.py should stay clean

```python
def register_user_command(use_case):
    name = input("Name: ")
    email = input("Email: ")
    use_case.execute(name, email)
```

Notice:

```
presentation does NOT import infrastructure
presentation does NOT create objects
```

It only:

```
talks to application
```

---

# Why your current design violates the rule

If you have:

```python
# presentation/cli.py
from infrastructure.db import SqlUserRepository  # ❌
```

then presentation is doing:

```
object creation + infrastructure knowledge
```

which breaks:

```
presentation → infrastructure
```

---

# How to fix your current project with minimal refactor

### Step 1: Rename cli.py

```
presentation/cli.py → presentation/commands.py
```

### Step 2: Add a new entrypoint

```
src/main.py
```

### Step 3: Move wiring to main.py

This is called:

```
Composition Root Pattern
```

---

# Visual architecture after fix

```
                main.py
                   │
                   ▼
presentation → application → domain
                   ▲
                   │
            infrastructure
```

All arrows still point inward except the bootstrapper, which is allowed.

---

# Why this pattern is industry standard

This is how dependency injection containers behave in:

* FastAPI
* Django
* ASP.NET
* Spring

They all have a:

```
startup / main / program.cs / app.py
```

file that wires dependencies.

---

# Rule of thumb

If a file:

```
creates concrete classes
```

it belongs in:

```
composition root
```

not in presentation or application.

---

# Minimal example directory

```
src/
├── main.py
├── domain/
├── application/
├── presentation/
│   └── cli_commands.py
└── infrastructure/
```

---

If you want, I can refactor your current project layout (based on the structure you used in previous messages) and generate a ready-to-run CLI template with dependency injection, import-linter rules, and tests.

---

adapters are equivalent to presentation?

---

Yes — in most Python Clean Architecture projects, **“adapters” and “presentation” are closely related, but not always identical**. The confusion comes from different terminology used in different diagrams and books. Let’s clarify precisely. 👇

---

# The original Clean Architecture terminology

In **Robert C. Martin’s Clean Architecture**, the outer layers are called:

```
Entities
Use Cases
Interface Adapters
Frameworks & Drivers
```

Here, **Interface Adapters** are **not only presentation** — they include **everything that converts data between layers**.

---

# What “Adapters” actually include

**Adapters = translation layer** between the outside world and the application.

They contain:

```
Adapters
├── Controllers (input)
├── Presenters / View models (output)
├── Gateways (repository adapters)
└── API serializers / DTO mappers
```

So adapters are **bigger than presentation**.

---

# Mapping to Python folder naming

Many Python repos rename layers to be more intuitive:

| Clean Architecture term | Common Python folder                                    |
| ----------------------- | ------------------------------------------------------- |
| Interface Adapters      | `presentation/` + `adapters/` + sometimes `interfaces/` |
| Frameworks & Drivers    | `infrastructure/`                                       |

So depending on the repo:

### Variant A (strict Uncle Bob naming)

```
src/
├── domain/
├── application/
├── adapters/
└── infrastructure/
```

### Variant B (web-app oriented naming)

```
src/
├── domain/
├── application/
├── presentation/   ← controllers, routes
└── infrastructure/ ← db, email, cache
```

Variant B is very common in FastAPI/Django projects because:

* developers think in terms of “presentation layer”
* adapters are split across folders

---

# Key conceptual difference

### Presentation is only **input/output for humans**

```
HTTP routes
CLI commands
GUI views
```

### Adapters also include **data source adapters**

```
SQLAlchemy repositories
Kafka consumers
REST API clients
```

So this repository structure:

```
presentation/
infrastructure/
```

actually splits the **adapter ring into two**:

```
[ Interface Adapters ]
     ├── presentation
     └── infrastructure
```

That’s why both names appear in different projects.

---

# Recommended naming (for clarity)

If you want to follow your rule matrix and avoid ambiguity, use:

```
src/
├── domain/
├── application/
├── presentation/     # controllers, routes, CLI
└── infrastructure/   # db, email, filesystem
```

This is the most readable structure in Python ecosystems and is widely used in FastAPI clean-architecture templates.

---

# Mental model to remember 🧭

```
Domain        = business rules
Application   = use cases
Adapters      = translation layer
Infrastructure= technical implementations
```

And:

```
presentation ⊂ adapters
infrastructure ⊂ adapters
```

So:

> **Adapters are a superset; presentation is a subset.**

---

# Practical dependency flow example

```
presentation → application → domain
                     ↓
              repository interface
                     ↓
             infrastructure implementation
```

This keeps the **Dependency Rule** intact while allowing you to name folders in a way that fits Python projects.

---

If you’d like, I can also generate an **import-linter configuration** that enforces this exact mapping (`presentation` and `infrastructure` both treated as adapters) so your CI will catch violations automatically.

---

now i have starting point of program in presentation/cli.py but it violates rule that cannot import from infrastructure

---

This is a **very common confusion** when implementing Clean Architecture in Python CLI apps — and you’re actually very close to the correct solution. 👍

Your situation:

```
presentation/cli.py  ← entrypoint
```

And you’re worried because:

```
presentation → infrastructure   ❌ forbidden
```

But your CLI must somehow **wire dependencies** (e.g., create DB repo, email client, etc.), which *are* infrastructure objects.

This is where **composition root** comes in.

---

# 🧠 Key principle: **The entrypoint is allowed to break the rule**

The Clean Architecture rule:

> Dependencies must point inward

applies to **application code**, not to the **startup script**.

The entrypoint is:

```
main.py
cli.py
app.py
```

and it is considered:

```
Frameworks & Drivers layer
```

which is **outside the architecture rings**.

So this is **allowed**:

```
cli.py → infrastructure → application → domain
```

because the entrypoint is not part of the “presentation layer” in the architectural sense — it is **bootstrap code**.

---

# Correct structure for a CLI Clean Architecture project

Recommended:

```
src/
├── domain/
├── application/
├── presentation/
│   └── cli_commands.py      # command handlers only
├── infrastructure/
└── main.py                  # composition root
```

### `main.py` responsibilities:

* create infrastructure objects
* wire them into use cases
* call presentation layer

---

# Example of correct dependency flow

### main.py (composition root)

```python
from infrastructure.db import SqlUserRepository
from infrastructure.email import SmtpEmailSender

from application.usecases.register_user import RegisterUser
from presentation.cli_commands import register_user_command


def main():
    repo = SqlUserRepository()
    email = SmtpEmailSender()

    use_case = RegisterUser(repo, email)

    register_user_command(use_case)


if __name__ == "__main__":
    main()
```

This file is **allowed** to import everything because:

```
it is not part of the architecture layers
```

---

# presentation/cli_commands.py should stay clean

```python
def register_user_command(use_case):
    name = input("Name: ")
    email = input("Email: ")
    use_case.execute(name, email)
```

Notice:

```
presentation does NOT import infrastructure
presentation does NOT create objects
```

It only:

```
talks to application
```

---

# Why your current design violates the rule

If you have:

```python
# presentation/cli.py
from infrastructure.db import SqlUserRepository  # ❌
```

then presentation is doing:

```
object creation + infrastructure knowledge
```

which breaks:

```
presentation → infrastructure
```

---

# How to fix your current project with minimal refactor

### Step 1: Rename cli.py

```
presentation/cli.py → presentation/commands.py
```

### Step 2: Add a new entrypoint

```
src/main.py
```

### Step 3: Move wiring to main.py

This is called:

```
Composition Root Pattern
```

---

# Visual architecture after fix

```
                main.py
                   │
                   ▼
presentation → application → domain
                   ▲
                   │
            infrastructure
```

All arrows still point inward except the bootstrapper, which is allowed.

---

# Why this pattern is industry standard

This is how dependency injection containers behave in:

* FastAPI
* Django
* ASP.NET
* Spring

They all have a:

```
startup / main / program.cs / app.py
```

file that wires dependencies.

---

# Rule of thumb

If a file:

```
creates concrete classes
```

it belongs in:

```
composition root
```

not in presentation or application.

---

# Minimal example directory

```
src/
├── main.py
├── domain/
├── application/
├── presentation/
│   └── cli_commands.py
└── infrastructure/
```

---

If you want, I can refactor your current project layout (based on the structure you used in previous messages) and generate a ready-to-run CLI template with dependency injection, import-linter rules, and tests.

---

propose refactor of this: https://github.com/pdob-git/clean-app/tree/arch_test

---

I reviewed your repository structure and README on the `arch_test` branch. It already follows Clean Architecture conceptually, but **the composition root and dependency direction are mixed into `presentation/cli.py`**, which is why you’re hitting rule violations. ([GitHub][1])

Below is a **concrete refactor proposal** that preserves your functionality while making the dependency rule formally correct and compatible with tools like `import-linter` or `pytestarch`.

---

# Current structure (from repo)

```
src/clean_app/
├── domain/
├── application/
├── infrastructure/
└── presentation/
    └── cli.py    ← entrypoint + wiring mixed
```

README confirms:

```
Presentation Layer (presentation/cli.py)
Application Layer
Domain Layer
Infrastructure Layer
```

This means:

```
cli.py → infrastructure
```

which violates your own rule:

```
presentation cannot import infrastructure
```

---

# Goal of refactor

We want to achieve:

```
composition root
        │
        ▼
presentation → application → domain
                       ▲
                       │
                infrastructure
```

And enforceable rules:

```
presentation cannot import infrastructure
application cannot import infrastructure
domain cannot import anything
```

---

# Proposed target structure

```
src/clean_app/
├── domain/
│   ├── entities/
│   └── repositories.py
│
├── application/
│   ├── usecases/
│   │   ├── get_users.py
│   │   └── export_data.py
│   └── ports/                # optional but recommended
│
├── presentation/
│   ├── cli/
│   │   ├── commands.py       # Click commands only
│   │   └── dto.py            # optional CLI DTO mapping
│
├── infrastructure/
│   ├── repositories/
│   │   └── sqlite_user_repo.py
│   └── exporters/
│
└── main.py                   # NEW composition root
```

---

# Step-by-step refactor

## 1. Split CLI responsibilities

### Current

```
presentation/cli.py
    - Click decorators
    - object construction
    - use case invocation
```

### After refactor

```
presentation/cli/commands.py
    - Click commands only
    - receives use cases as parameters
```

---

## 2. Create composition root

### `src/clean_app/main.py`

This file wires everything:

```python
from clean_app.infrastructure.sqlite_repo import SQLiteUserRepository
from clean_app.infrastructure.exporters import EXPORTERS

from clean_app.application.get_users import GetUsersUseCase
from clean_app.application.export_data import ExportDataUseCase

from clean_app.presentation.cli.commands import cli


def build_cli():
    repo = SQLiteUserRepository()

    get_users = GetUsersUseCase(repo)
    export = ExportDataUseCase(repo, EXPORTERS)

    cli.obj = {
        "get_users": get_users,
        "export": export,
    }
    return cli


def main():
    app = build_cli()
    app()


if __name__ == "__main__":
    main()
```

Now:

```
main.py → infrastructure ✔ allowed
```

---

## 3. Refactor Click commands

### New `presentation/cli/commands.py`

```python
import click


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.pass_context
def get_users(ctx):
    use_case = ctx.obj["get_users"]
    users = use_case.execute()
    for u in users:
        click.echo(f"{u.id} {u.name}")
```

Notice:

```
presentation imports only application interfaces
```

No infrastructure imports.

---

## 4. Move exporter registry

Currently:

```
infrastructure/exporters/__init__.py
EXPORTERS = { ... }
```

This forces:

```
application → infrastructure
```

Instead, move the registry to composition root:

```python
from clean_app.infrastructure.exporters.csv_exporter import CsvExporter
from clean_app.infrastructure.exporters.excel_exporter import ExcelExporter

exporters = {
    "csv": CsvExporter(),
    "excel": ExcelExporter(),
}
```

Then inject into:

```
ExportDataUseCase(exporters)
```

This preserves **Open/Closed** without violating DIP.

---

# Final dependency graph

After refactor:

```
main.py
   │
   ├── infrastructure
   ├── application
   └── presentation

presentation → application → domain
infrastructure → domain
```

This **exactly matches** Clean Architecture rule matrix.

---

# import-linter rules you’ll now be able to enforce

```ini
[importlinter:contract:layers]
name = clean_architecture
layers =
    domain
    application
    presentation
    infrastructure
```

and forbidden:

```
presentation -> infrastructure
application -> infrastructure
domain -> *
```

Before refactor this contract would fail; after it will pass.

---

# Additional improvements I recommend

## 1. Move use cases into subpackage

```
application/
    usecases/
```

This makes scaling easier when you reach 20–30 use cases.

---

## 2. Rename repositories.py

Currently:

```
domain/repositories.py
```

Better:

```
domain/repositories/user_repository.py
```

This avoids “God interface files”.

---

## 3. Introduce DTO boundary (optional but advanced)

CLI currently prints domain objects directly. Cleanest architecture:

```
domain entity → application DTO → presentation view model
```

Not required now, but useful if you later add REST API.

---

# Summary of concrete file moves

| Old                                           | New                          |
| --------------------------------------------- | ---------------------------- |
| presentation/cli.py                           | presentation/cli/commands.py |
| —                                             | main.py                      |
| infrastructure/exporters/**init**.py registry | main.py                      |
| application/*.py                              | application/usecases/*.py    |

---

# Why this refactor matters

After it:

* your project will pass architecture linting
* presentation layer will be framework-agnostic
* you can add REST API alongside CLI without touching application
* unit tests for CLI become trivial (just inject fake use cases)

---

If you want, I can generate a **ready pull-request style patch** showing exact diffs for every file so you can apply the refactor in one commit.

[1]: https://github.com/pdob-git/clean-app/tree/arch_test "GitHub - pdob-git/clean-app at arch_test · GitHub"

---
