# AGENTS.md

This file contains development guidelines for agentic coding agents working in this Python microservice repository.

## Development Environment Setup

Use `uv` as the package manager. The project uses Python 3.10+.

```bash
# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Optional: Set up environment variables (database, authentication, logging, OpenTelemetry, etc.)
cp .env.example .env
# Edit .env to configure DATABASE_URL, API_TOKENS, LOG_LEVEL, and/or OTEL_* variables
```

## Build/Lint/Test Commands

### Testing

```bash
# Run all tests with coverage (require 100% coverage)
uv run coverage run -m pytest && uv run coverage report

# Run specific test file
uv run pytest tests/test_main.py

# Run specific test function
uv run pytest tests/test_main.py::test_read_root

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage HTML report
uv run coverage html
```

### Linting & Formatting

```bash
# Format code
uv run black .

# Check formatting without changing files
uv run black --check .

# Check imports without changing files
uv run isort --check-only .

# Sort imports
uv run isort .

# Lint code
uv run ruff check

# Auto-fix linting issues
uv run ruff check --fix

# Type checking with pyright
uv run pyright

# Run all pre-commit hooks (quality checks)
uv run pre-commit run --all-files
```

### Development Server

```bash
# Run in development mode (with auto-reload)
uv run fastapi dev

# Alternative: Run with uvicorn directly (development)
uv run uvicorn app.main:app --reload

# Run in production mode
uv run fastapi run

# Alternative: Run with uvicorn directly (production)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Database Migrations (Optional)

```bash
# Create a new migration after modifying models
uv run alembic revision --autogenerate -m "description of changes"

# Apply all pending migrations
uv run alembic upgrade head

# Rollback last migration
uv run alembic downgrade -1

# View migration history
uv run alembic history

# Check current migration version
uv run alembic current
```

## Code Style Guidelines

### Import Organization

- Use `collections.abc` for collection abstract base classes
- Standard library imports first, then third-party, then local imports
- Use `isort` to maintain consistent import ordering
- Use absolute imports for local modules (e.g., `from app.main import app`)
- Use `# isort: skip` to skip sorting for specific import lines (e.g., when models need to be imported for side effects)
- Use `# isort: skip_file` at the top of a file to skip the entire file

### Type Annotations

- All functions must have explicit type annotations
- Use modern union syntax: `str | None` instead of `Optional[str]`
- Use generic dict syntax: `dict[str, str]` instead of `Dict[str, str]`
- Enable strict MyPy mode - all code must pass strict type checking

### Naming Conventions

- `snake_case` for variables, functions, and files
- `PascalCase` for classes and Pydantic models
- `UPPER_SNAKE_CASE` for constants
- Router instances: `router`
- FastAPI app instance: `app`
- Test client fixture: `client`

### Code Structure

- Use APIRouter for modular endpoint organization
- Include routers in main.py with descriptive prefixes
- Keep Pydantic models simple and focused
- Return types should be explicit in route handlers

### Authentication (Optional)

- Bearer token authentication is optional and controlled by `API_TOKENS` environment variable
- When enabled, protected endpoints require `Authorization: Bearer <token>` header
- Supports multiple tokens (comma-separated in environment variable)
- Protected routers are only included if authentication is enabled
- Use `BearerToken` dependency for protected endpoints: `from app.auth import BearerToken`
- Example: `def protected_endpoint(token: BearerToken) -> dict[str, str]:`

### Database (Optional)

- Database integration is optional and controlled by `DATABASE_URL` environment variable
- Use SQLModel for type-safe database models
- All SQLModel models should inherit from `SQLModel` with `table=True`
- Use Alembic for database migrations
- Follow naming convention: model classes are singular (e.g., `User`, not `Users`)
- Database session dependency: `from app.database import get_session`
- Migration files are auto-formatted with Black and Ruff via post-write hooks

### Logging

- Structured JSON logging is configured by default for better log aggregation and parsing
- Log level can be controlled via `LOG_LEVEL` environment variable (defaults to `INFO`)
- Supported log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Get a logger for your module: `from app.logging_config import get_logger; logger = get_logger(__name__)`
- All logs are output in JSON format with timestamp, level, logger name, message, and source location
- HTTP request/response middleware automatically logs all API requests
- Startup and shutdown events are logged
- Exception details (type, message, traceback) are automatically included in error logs

### OpenTelemetry (Optional)

- OpenTelemetry instrumentation is optional and controlled by `OTEL_ENABLED` environment variable
- When enabled, FastAPI is automatically instrumented for distributed tracing and metrics
- Requires `OTEL_EXPORTER_OTLP_ENDPOINT` to be set for data export (e.g., `http://localhost:4317` for local Jaeger)
- Service name can be customized via `OTEL_SERVICE_NAME` (defaults to `python-microservice-template`)
- Supports any OTLP-compatible backend: Jaeger, Grafana Cloud, Datadog, Honeycomb, etc.
- Initialization happens during application startup in `lifespan` handler
- Use `from app.otel import is_otel_enabled` to check if OpenTelemetry is enabled
- Logs warnings if enabled but endpoint is not configured

### Error Handling

- Raise FastAPI HTTPException for HTTP errors
- Use `B904` ruff exception (allow raising without from e for HTTPException)
- No print statements in production code (T201 ruff rule)

### Code Quality Rules

- Maximum line length: 88 characters (Black default)
- No unused function arguments (ARG001 ruff rule)
- Use pyupgrade-compatible code (UP ruff rules)
- Prefer comprehensions over loops where appropriate (C4 ruff rule)
- Avoid bug-prone patterns (B ruff rules)

### Testing Guidelines

- Use pytest for all testing
- Test client should be a module-scoped fixture
- Each test function should be focused on one behavior
- Use descriptive test names starting with `test_`
- Assert on both status codes and response content
- Include type annotations for test functions: `def test_function() -> None:`
- **100% test coverage is enforced** - `fail_under = 100` in pyproject.toml
- Use `# pragma: no cover` for lines that are impossible/impractical to test (e.g., module-level initialization based on environment variables)
- Add type hints for test fixtures to avoid pyright errors: `-> Generator[TestClient, None, None]`
- Use `# isort: skip` for imports that need specific ordering (e.g., model imports for SQLAlchemy registration)

### Documentation

- All API endpoints should have proper FastAPI documentation via docstrings
- Use clear, descriptive variable names
- Keep functions focused and small
- Return types should be self-documenting

### Performance Guidelines

- Use fast=True for Black formatting
- Use uv for fast dependency management
- Enable coverage dynamic context for better test insights

## Git Commit Guidelines

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Scope (Optional)

The scope provides additional contextual information:
- `(api)`: Changes to API endpoints
- `(auth)`: Changes to authentication
- `(db)`: Changes to database models or migrations
- `(logging)`: Changes to logging configuration
- `(otel)`: Changes to OpenTelemetry instrumentation
- `(tests)`: Changes to test files
- `(deps)`: Dependency updates

### Breaking Changes

Breaking changes should be indicated by:
- Adding `!` after the type/scope: `feat!: remove deprecated endpoint`
- Adding `BREAKING CHANGE:` in the footer

### Examples

```
feat(api): add user profile endpoint

fix(auth): resolve token validation issue

docs(readme): update installation instructions

test: add tests for healthcheck endpoint

build(deps): upgrade FastAPI to 0.109.0

refactor(db)!: change User model primary key type

BREAKING CHANGE: User.id is now UUID instead of int
```

### Best Practices

- Use the imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter of the description
- No period (.) at the end of the description
- Limit the description to 72 characters or less
- Reference issue numbers in the footer when applicable

## Project Structure

```
app/
├── __init__.py
├── main.py          # FastAPI app initialization and router includes
├── auth.py          # Optional bearer token authentication
├── protected.py     # Protected endpoints (requires auth)
├── database.py      # Optional database configuration
├── models.py        # SQLModel database models (example)
├── users.py         # User CRUD endpoints (requires database)
├── healthcheck.py   # Health check endpoints
├── items.py         # Item-related endpoints
├── logging_config.py # JSON logging configuration
└── otel.py          # Optional OpenTelemetry instrumentation

alembic/
├── versions/        # Database migration files
└── env.py           # Alembic environment configuration

tests/
├── __init__.py
├── conftest.py      # Pytest fixtures
├── test_main.py     # Main app tests
├── test_healthcheck.py  # Health check tests
├── test_items.py    # Item endpoints tests
├── test_logging_config.py  # Logging configuration tests
└── test_otel.py     # OpenTelemetry configuration tests
```

## Key Configuration Files

- `pyproject.toml`: Main project configuration, tool settings (Black, isort, Ruff, Pyright, Coverage, MyPy)
- `.pre-commit-config.yaml`: Pre-commit hooks configuration
- `uv.lock`: Dependency lock file (do not edit manually)
- `.env`: Environment variables (not in version control, copy from `.env.example`)
- `alembic.ini`: Alembic migration configuration

## Tool Configuration

### Black
- Line length: 88 characters (default)
- Fast mode enabled

### isort
- Profile: black (compatible with Black formatting)
- Line length: 88 characters

### Ruff
- Target: Python 3.10+
- Selected rules: pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, pyupgrade
- Enforces: no unused arguments, no print statements, proper exception handling

### Pyright
- Strict type checking for `app/` directory
- Reports unused imports, incorrect types, and type mismatches

### Coverage
- Enforces 100% code coverage (`fail_under = 100`)
- Tracks per-test coverage with dynamic context

## Optional Features

The microservice supports optional features that can be enabled via environment variables:

1. **Authentication** - Set `API_TOKENS` to enable bearer token authentication
   - Protected endpoints will only be included if tokens are configured
   - Multiple tokens can be comma-separated

2. **Database** - Set `DATABASE_URL` to enable database support
   - Database-dependent routers (like `/users`) only load if DB is configured
   - Supports PostgreSQL (production) and SQLite (development)
   - Migrations managed with Alembic

3. **OpenTelemetry** - Set `OTEL_ENABLED=true` to enable distributed tracing and metrics
   - Automatic instrumentation of FastAPI endpoints
   - Exports traces and metrics to OTLP-compatible backends (Jaeger, Grafana, Datadog, etc.)
   - Configured via `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable
   - Service name customizable via `OTEL_SERVICE_NAME` (defaults to 'python-microservice-template')

## Code Quality Standards

The project enforces strict code quality standards:

- **Black** - Code formatting with 88 character line length
- **isort** - Import sorting and organization
- **Ruff** - Fast Python linting with auto-fix support
- **Pyright** - Strict type checking for `app/` directory
- **Coverage** - 100% test coverage enforced via `fail_under = 100`
- **Pre-commit hooks** - Automatically run checks before each commit

All checks must pass before code can be merged:

```bash
# Run all quality checks
uv run black --check .
uv run isort --check-only .
uv run ruff check
uv run pyright
uv run coverage run -m pytest && uv run coverage report
```

## Notes

- The project is configured for Python 3.10+ with modern type annotations
- Coverage reports are automatically generated and uploaded to Codecov
- Any code that drops coverage below 100% will fail CI/CD checks
