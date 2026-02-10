# python-microservice-template

[![codecov](https://codecov.io/gh/remarkablemark/python-microservice-template/graph/badge.svg?token=RBdotUNGnY)](https://codecov.io/gh/remarkablemark/python-microservice-template)
[![test](https://github.com/remarkablemark/python-microservice-template/actions/workflows/test.yml/badge.svg)](https://github.com/remarkablemark/python-microservice-template/actions/workflows/test.yml)
[![lint](https://github.com/remarkablemark/python-microservice-template/actions/workflows/lint.yml/badge.svg)](https://github.com/remarkablemark/python-microservice-template/actions/workflows/lint.yml)

🐍 Python microservice template built with:

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://uvicorn.dev/)

## Prerequisites

[uv](https://docs.astral.sh/uv/#installation):

```sh
brew install uv
```

## Install

Clone the repository:

```sh
git clone https://github.com/remarkablemark/python-microservice-template.git
cd python-microservice-template
```

Install the dependencies:

```sh
uv sync
```

## Authentication

The microservice supports optional bearer token authentication.

### Enable Authentication

Copy the example environment file and configure your API tokens:

```sh
cp .env.example .env
```

Edit `.env` and set your bearer tokens:

```sh
# Single token
API_TOKENS=your-secret-token-here

# Multiple tokens (comma-separated)
API_TOKENS=token-1,token-2,token-3
```

### Using Protected Endpoints

Protected endpoints require an `Authorization` header with a bearer token:

```sh
curl -H "Authorization: Bearer your-secret-token-here" \
  http://127.0.0.1:8000/protected/
```

When authentication is enabled, the `/protected` endpoints will be available at:
- `GET /protected/` - Basic protected endpoint
- `GET /protected/data` - Protected endpoint with data

## Database

The microservice supports optional database integration using SQLModel and Alembic.

### Environment Variables

Copy the example environment file and configure your database:

```sh
cp .env.example .env
```

Edit `.env` and set your database URL:

```sh
# For SQLite (Development)
DATABASE_URL=sqlite:///./app.db

# For PostgreSQL (Production)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Migrations

Create a new migration after modifying models:

```sh
uv run alembic revision --autogenerate -m "description"
```

Apply migrations:

```sh
uv run alembic upgrade head
```

Rollback migration:

```sh
uv run alembic downgrade -1
```

## Available Scripts

In the project directory, you can run:

### `uv run pre-commit install`

Installs the pre-commit script.

### `uv run fastapi dev`

Runs the app in development mode:

- Server: http://127.0.0.1:8000
- Documentation: http://127.0.0.1:8000/docs

The server will reload if you make edits.

Alternatively, run with uvicorn directly:

```sh
uv run uvicorn app.main:app --reload
```

### `uv run fastapi run`

Runs the app in production mode.

Alternatively, run with uvicorn directly:

```sh
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### `uv run black .`

Formats the code.

### `uv run isort .`

Sorts and organizes imports.

### `uv run ruff check`

Lints the code.

### `uv run coverage run -m pytest && uv run coverage report`

Runs tests with coverage reporting (fails if coverage is below 100%).

### `uv run alembic revision --autogenerate -m "message"`

Creates a new database migration.

### `uv run alembic upgrade head`

Applies all pending database migrations.

## License

[MIT](https://github.com/remarkablemark/python-microservice-template/blob/master/LICENSE)
