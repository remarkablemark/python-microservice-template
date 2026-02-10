# AGENTS.md

This file contains development guidelines for agentic coding agents working in this Python microservice repository.

## Development Environment Setup

Use `uv` as the package manager. The project uses Python 3.10+.

```bash
# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Optional: Set up database (copy .env.example to .env and configure DATABASE_URL)
cp .env.example .env
```

## Build/Lint/Test Commands

### Testing

```bash
# Run all tests with coverage
uv run coverage run -m pytest
uv run coverage report

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

# Sort imports
uv run isort .

# Lint code
uv run ruff check

# Auto-fix linting issues
uv run ruff check --fix

# Type checking with pyright
uv run pyright

# Run all pre-commit hooks
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

### Database (Optional)

- Database integration is optional and controlled by `DATABASE_URL` environment variable
- Use SQLModel for type-safe database models
- All SQLModel models should inherit from `SQLModel` with `table=True`
- Use Alembic for database migrations
- Follow naming convention: model classes are singular (e.g., `User`, not `Users`)
- Database session dependency: `from app.database import get_session`
- Migration files are auto-formatted with Black and Ruff via post-write hooks

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
- Enforce 100% test coverage

### Documentation

- All API endpoints should have proper FastAPI documentation via docstrings
- Use clear, descriptive variable names
- Keep functions focused and small
- Return types should be self-documenting

### Performance Guidelines

- Use fast=True for Black formatting
- Use uv for fast dependency management
- Enable coverage dynamic context for better test insights

## Project Structure

```
app/
├── __init__.py
├── main.py          # FastAPI app initialization and router includes
├── database.py      # Optional database configuration
├── models.py        # SQLModel database models (example)
├── healthcheck.py   # Health check endpoints
└── items.py         # Item-related endpoints

alembic/
├── versions/        # Database migration files
└── env.py           # Alembic environment configuration

tests/
├── __init__.py
├── conftest.py      # Pytest fixtures
├── test_main.py     # Main app tests
├── test_healthcheck.py  # Health check tests
└── test_items.py    # Item endpoints tests
```

## Key Configuration Files

- `pyproject.toml`: Main project configuration, tool settings
- `.pre-commit-config.yaml`: Pre-commit hooks configuration
- `uv.lock`: Dependency lock file (do not edit manually)
- `.env`: Environment variables (not in version control, copy from `.env.example`)
- `alembic.ini`: Alembic migration configuration

## Notes

- The project follows strict code quality standards enforced by pre-commit hooks
- All code must pass Black formatting, Ruff linting, and MyPy type checking
- Coverage reports are automatically generated and uploaded to Codecov
- The project is configured for Python 3.10+ with modern type annotations
