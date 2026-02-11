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
uv run pytest tests/api/routes/test_healthcheck.py

# Run specific test function
uv run pytest tests/api/routes/test_healthcheck.py::test_healthcheck

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage HTML report
uv run coverage html
```

### Linting & Formatting

```bash
# Format code and sort imports
uv run ruff format

# Check formatting without changing files
uv run ruff format --check

# Lint code (includes import sorting check)
uv run ruff check

# Auto-fix linting issues (includes import sorting)
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
- Use Ruff's import sorting to maintain consistent import ordering
- Use absolute imports for local modules (e.g., `from app.main import app`)

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
- All API routes except healthcheck are versioned under `/v1` prefix
- V1 routes are organized in `app/api/routes/v1/` directory with a consolidated router
- Healthcheck endpoint remains at root (`/`) for infrastructure monitoring
- Keep Pydantic models simple and focused
- Return types should be explicit in route handlers

### Authentication (Optional)

- Bearer token authentication is optional and controlled by `API_TOKENS` environment variable
- When enabled, protected endpoints require `Authorization: Bearer <token>` header
- Supports multiple tokens (comma-separated in environment variable)
- Protected routers are only included if authentication is enabled
- Use `BearerToken` dependency for protected endpoints: `from app.core.auth import BearerToken`
- Example: `def protected_endpoint(token: BearerToken) -> dict[str, str]:`

### Database (Optional)

- Database integration is optional and controlled by `DATABASE_URL` environment variable
- Use SQLModel for type-safe database models
- All SQLModel models should inherit from `SQLModel` with `table=True`
- Use Alembic for database migrations
- Follow naming convention: model classes are singular (e.g., `User`, not `Users`)
- Database session dependency: `from app.core.database import get_session`
- Migration files are auto-formatted with Ruff via post-write hooks

### Logging

- Structured JSON logging is configured by default for better log aggregation and parsing
- Log level can be controlled via `LOG_LEVEL` environment variable (defaults to `INFO`)
- Supported log levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Get a logger for your module: `from app.core.logging_config import get_logger; logger = get_logger(__name__)`
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
- Use `from app.core.otel import is_otel_enabled` to check if OpenTelemetry is enabled
- Logs warnings if enabled but endpoint is not configured

### Error Handling

- Use exception factory functions from `app.core.exceptions` for consistent error responses
- Available factories: `not_found_exception()`, `bad_request_exception()`, `unauthorized_exception()`, `forbidden_exception()`, `internal_server_exception()`
- Only create HTTPException directly if none of the factories fit your use case
- Use `B904` ruff exception (allow raising without from e for HTTPException)
- No print statements in production code (T201 ruff rule)

### Code Quality Rules

- Maximum line length: 88 characters
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
- **Use test utilities from `tests/utils/`** to reduce boilerplate and maintain consistency:
  - `database.py` for test database setup
  - `auth.py` for authentication token management
  - `env.py` for environment variable management
  - `app_factory.py` for creating test FastAPI applications
- **Avoid code duplication in tests** - use parameterized tests (`@pytest.mark.parametrize`) for similar test cases
- **Create helper functions** for repetitive test operations (e.g., creating test users)

### Documentation

- All API endpoints should have proper FastAPI documentation via docstrings
- Use clear, descriptive variable names
- Keep functions focused and small
- Return types should be self-documenting

### Performance Guidelines

- Use uv for fast dependency management
- Enable coverage dynamic context for better test insights

## Reusable Utilities & DRY Principles

This project follows the **DRY (Don't Repeat Yourself)** principle to maintain code quality and reduce duplication. Several reusable utility modules have been created to support this.

### Application Utilities (`app/core/`)

#### Exception Factories (`app/core/exceptions.py`)

Standardized HTTP exception creation for consistent error responses:

```python
from app.core.exceptions import (
    not_found_exception,
    bad_request_exception,
    unauthorized_exception,
    forbidden_exception,
    internal_server_exception,
)

# Usage examples
raise not_found_exception("User", user_id)  # 404
raise bad_request_exception("Email already exists")  # 400
raise unauthorized_exception("Missing bearer token")  # 401
raise forbidden_exception("Access denied")  # 403
raise internal_server_exception("Database not configured")  # 500
```

**When to use:** Always use these factories instead of creating HTTPException instances directly. This ensures consistent status codes and error message formatting across the application.

#### Environment Variable Utilities (`app/core/env.py`)

Type-safe environment variable retrieval:

```python
from app.core.env import get_env_bool, get_env_str, get_env_list

# Boolean values (case-insensitive "true" = True)
debug_mode = get_env_bool("DEBUG", default=False)
otel_enabled = get_env_bool("OTEL_ENABLED")

# String values with defaults
log_level = get_env_str("LOG_LEVEL", "INFO")
service_name = get_env_str("SERVICE_NAME", "my-service")

# Comma-separated lists
api_tokens = get_env_list("API_TOKENS")
allowed_hosts = get_env_list("ALLOWED_HOSTS", separator=";")
```

**When to use:** Always use these utilities instead of `os.getenv()` directly. They provide type safety, consistent parsing, and default value handling.

#### Database Query Utilities (`app/core/db_utils.py`)

Common database query patterns:

```python
from app.core.db_utils import get_by_id_or_404, exists_by_field

# Get by ID or raise 404
user = get_by_id_or_404(session, User, user_id, "User")

# Check if field value exists
if exists_by_field(session, User, "email", "test@example.com"):
    raise bad_request_exception("Email already exists")
```

**When to use:** Use `get_by_id_or_404()` for all ID-based lookups in endpoints. Use `exists_by_field()` for duplicate checking before creating records.

### Test Utilities (`tests/utils/`)

#### Database Test Utilities (`tests/utils/database.py`)

Simplify database setup in tests:

```python
from tests.utils.database import create_test_engine, temporary_test_engine

# Create a standard test engine
engine = create_test_engine()

# Temporarily override module's engine (with automatic cleanup)
with temporary_test_engine(database_module) as engine:
    database_module.create_db_and_tables()
    # ... run tests ...
```

**When to use:** Use `create_test_engine()` for standard SQLite test databases. Use `temporary_test_engine()` when testing code that accesses the global engine.

#### Auth Test Utilities (`tests/utils/auth.py`)

Manage authentication tokens in tests:

```python
from tests.utils.auth import temporary_valid_tokens, create_auth_header

# Temporarily set authentication tokens
with temporary_valid_tokens(auth_module, {"test-token", "another-token"}):
    # ... run tests with auth enabled ...

# Create authorization headers
headers = create_auth_header("my-token")
response = client.get("/protected", headers=headers)
```

**When to use:** Use `temporary_valid_tokens()` for all auth-related tests. Use `create_auth_header()` instead of manually creating header dictionaries.

#### Environment Variable Test Utilities (`tests/utils/env.py`)

Manage environment variables in tests:

```python
from tests.utils.env import temporary_env_vars, clean_env_vars

# Set environment variables temporarily
with temporary_env_vars(LOG_LEVEL="DEBUG", DATABASE_URL=None):
    # ... run tests ...

# Clear specific environment variables
with clean_env_vars("OTEL_ENABLED", "OTEL_EXPORTER_OTLP_ENDPOINT"):
    # ... run tests without these variables ...
```

**When to use:** Always use these utilities instead of manually modifying `os.environ`. They ensure proper cleanup and isolation between tests.

#### Test App Factory (`tests/utils/app_factory.py`)

Create FastAPI test applications:

```python
from tests.utils.app_factory import create_test_app_with_database, create_test_app_with_lifespan

# Create test app with database session override
app = create_test_app_with_database(
    db_session,
    include_routers=[(users_router, {"prefix": "/users"})]
)

# Create test app with custom lifespan
app = create_test_app_with_lifespan(my_lifespan_handler)
```

**When to use:** Use these factories instead of creating FastAPI apps manually in test fixtures. They handle common setup patterns consistently.

### DRY Best Practices

1. **Avoid Duplicate Code**
   - If you write the same code twice, create a reusable function or utility
   - Extract common test setup into fixtures or helper functions
   - Use parameterized tests (`@pytest.mark.parametrize`) for similar test cases

2. **Use Helper Functions**
   - Create test helper functions for repetitive operations (e.g., creating test users)
   - Keep helpers in the same test file for file-specific patterns
   - Move to `tests/utils/` if used across multiple test files

3. **Leverage Existing Utilities**
   - Always check `app/core/` and `tests/utils/` before writing similar code
   - Prefer utilities over inline implementations for consistency
   - Extend existing utilities rather than duplicating patterns

4. **Maintain Readability**
   - Utilities should make code more readable, not more obscure
   - Use descriptive names that clearly indicate what the utility does
   - Add comprehensive docstrings with usage examples

5. **Test Your Utilities**
   - All utilities must have 100% test coverage
   - Test both success and failure paths
   - Document expected behavior in tests

### Example: Refactoring for DRY

**Before (Duplicate Code):**

```python
# In multiple test files
def test_create_user():
    response = client.post("/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
    })
    # ... assertions ...

def test_update_user():
    # Same user creation code repeated
    response = client.post("/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
    })
    user_id = response.json()["id"]
    # ... rest of test ...
```

**After (DRY with Helper):**

```python
# Helper function at top of test file
def create_test_user(client, email, username, full_name):
    """Helper to create a test user."""
    response = client.post("/users/", json={
        "email": email,
        "username": username,
        "full_name": full_name,
    })
    return response.json()

def test_create_user():
    user = create_test_user(client, "test@example.com", "testuser", "Test User")
    # ... assertions ...

def test_update_user():
    user = create_test_user(client, "test@example.com", "testuser", "Test User")
    # ... rest of test ...
```

### Reusability Checklist

When adding new code, ask yourself:

- [ ] Is this pattern used elsewhere in the codebase?
- [ ] Could this be extracted into a reusable utility?
- [ ] Does a similar utility already exist that I can use?
- [ ] Will this code be needed in multiple places?
- [ ] Is the function properly documented with usage examples?
- [ ] Does the utility have 100% test coverage?

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
├── main.py              # FastAPI app initialization and router includes
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── healthcheck.py  # Health check endpoint (root path)
│       └── v1/             # V1 API routes (all under /v1 prefix)
│           ├── __init__.py     # V1 router aggregator
│           ├── items.py        # Item-related endpoints
│           ├── protected.py    # Protected endpoints (requires auth)
│           └── users.py        # User CRUD endpoints (requires database)
├── core/
│   ├── __init__.py
│   ├── auth.py          # Optional bearer token authentication
│   ├── database.py      # Optional database configuration
│   ├── db_utils.py      # Reusable database query utilities
│   ├── env.py           # Type-safe environment variable utilities
│   ├── exceptions.py    # HTTP exception factory functions
│   ├── logging_config.py # JSON logging configuration
│   ├── metadata.py      # Project metadata
│   └── otel.py          # Optional OpenTelemetry instrumentation
└── models/
    ├── __init__.py
    └── user.py          # SQLModel database models (example)

alembic/
├── versions/        # Database migration files
└── env.py           # Alembic environment configuration

tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── test_healthcheck.py  # Health check tests (root path)
│       └── v1/                  # V1 API route tests
│           ├── __init__.py
│           ├── test_items.py    # Item endpoints tests
│           └── test_users.py    # User CRUD tests
├── core/
│   ├── __init__.py
│   ├── test_auth.py             # Authentication tests
│   ├── test_database.py         # Database configuration tests
│   ├── test_db_utils.py         # Database utility tests
│   ├── test_env.py              # Environment variable utility tests
│   ├── test_exceptions.py       # Exception factory tests
│   ├── test_logging_config.py   # Logging configuration tests
│   └── test_otel.py             # OpenTelemetry configuration tests
├── integration/
│   ├── __init__.py
│   └── test_main.py     # Integration tests
└── utils/
    ├── __init__.py
    ├── app_factory.py       # FastAPI test app factory utilities
    ├── auth.py              # Authentication test utilities
    ├── database.py          # Database test utilities
    └── env.py               # Environment variable test utilities
```

## Key Configuration Files

- `pyproject.toml`: Main project configuration, tool settings (Ruff, Pyright, Coverage, MyPy)
- `.pre-commit-config.yaml`: Pre-commit hooks configuration
- `uv.lock`: Dependency lock file (do not edit manually)
- `.env`: Environment variables (not in version control, copy from `.env.example`)
- `alembic.ini`: Alembic migration configuration

## Tool Configuration

### Ruff

- **Formatting**: Black-compatible code formatter with 88 character line length
- **Import sorting**: Replaces isort, maintains standard library → third-party → local import order
- **Linting**: Target Python 3.10+
- **Selected rules**: pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, pyupgrade
- **Enforces**: no unused arguments, no print statements, proper exception handling, sorted imports

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
   - Service name customizable via `OTEL_SERVICE_NAME` (defaults to project name from pyproject.toml)

## Code Quality Standards

The project enforces strict code quality standards:

- **Ruff** - Fast Python formatter, import sorter, and linter (replaces Black + isort + Flake8)
- **Pyright** - Strict type checking for `app/` directory
- **Coverage** - 100% test coverage enforced via `fail_under = 100`
- **Pre-commit hooks** - Automatically run checks before each commit

All checks must pass before code can be merged:

```bash
# Run all quality checks
uv run ruff format --check
uv run ruff check
uv run pyright
uv run coverage run -m pytest && uv run coverage report
```

## Notes

- The project is configured for Python 3.10+ with modern type annotations
- Coverage reports are automatically generated and uploaded to Codecov
- Any code that drops coverage below 100% will fail CI/CD checks
