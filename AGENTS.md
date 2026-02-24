# AGENTS.md

Development guidelines for this Python FastAPI microservice (Python 3.10+, uv).

## Quick Start

```bash
uv sync && uv run pre-commit install && cp .env.example .env
uv run fastapi dev  # Development
```

## Commands

```bash
# Test (100% coverage required)
uv run coverage run -m pytest && uv run coverage report

# Lint & Format
uv run ruff format && uv run ruff check --fix
uv run pyright

# Pre-commit
uv run pre-commit run --all-files

# Database (optional)
uv run alembic revision --autogenerate -m "message" && uv run alembic upgrade head
```

## Code Style

- **Imports**: `collections.abc`, stdlib → third-party → local, absolute imports
- **Types**: `str | None`, `dict[str, str]`, strict Pyright
- **Naming**: `snake_case` (vars/functions), `PascalCase` (classes), `router`, `app`, `client`
- **Line length**: 88 chars
- No unused args, no print statements

## Optional Features

| Feature | Env Variable | Notes |
|---------|--------------|-------|
| Auth | `API_KEYS` | Bearer token, comma-separated |
| Database | `DATABASE_URL` | SQLModel + Alembic |
| Tracing | `OTEL_ENABLED` | Requires `OTEL_EXPORTER_OTLP_ENDPOINT` |

## Key Utilities

```python
# Exceptions
from app.core.exceptions import not_found_exception, bad_request_exception
raise not_found_exception("User", user_id)

# Env vars
from app.core.env import get_env_bool, get_env_str, get_env_list

# Logging
from app.core.logging_config import get_logger
logger = get_logger(__name__)

# DB utils
from app.core.db_utils import get_by_id_or_404, exists_by_field
```

## Test Utilities

```python
from tests.utils.database import create_test_engine, temporary_test_engine
from tests.utils.auth import temporary_valid_tokens, create_auth_header
from tests.utils.env import temporary_env_vars, clean_env_vars
from tests.utils.app_factory import create_test_app_with_database
```

## Testing

- 100% coverage required (`fail_under = 100`)
- Use `@pytest.mark.parametrize` for similar cases
- Create helper functions for repetitive operations
- Use `tests/utils/` utilities

## Git Commits

```
<type>[scope]: <description>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
```

## Project Structure

```
app/
├── main.py              # FastAPI app
├── api/routes/
│   ├── healthcheck.py   # Root path /
│   └── v1/             # /v1/* (items, users, protected)
└── core/               # auth, database, env, exceptions, logging, otel

tests/
├── api/routes/v1/
├── core/               # Unit tests
├── integration/
└── utils/              # Test helpers
```

## Quality Checks

All must pass:
```bash
uv run ruff format --check && uv run ruff check && uv run pyright && uv run coverage run -m pytest
```
