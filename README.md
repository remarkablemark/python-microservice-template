# python-microservice-template

[![codecov](https://codecov.io/gh/remarkablemark/python-microservice-template/graph/badge.svg?token=RBdotUNGnY)](https://codecov.io/gh/remarkablemark/python-microservice-template)
[![test](https://github.com/remarkablemark/python-microservice-template/actions/workflows/test.yml/badge.svg)](https://github.com/remarkablemark/python-microservice-template/actions/workflows/test.yml)
[![lint](https://github.com/remarkablemark/python-microservice-template/actions/workflows/lint.yml/badge.svg)](https://github.com/remarkablemark/python-microservice-template/actions/workflows/lint.yml)

⚡ [FastAPI](https://fastapi.tiangolo.com/) template inspired by [Full Stack FastAPI Template](https://fastapi.tiangolo.com/project-generation/).

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

## Available Scripts

In the project directory, you can run:

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

### `uv run pre-commit install`

Installs the pre-commit script.

### `uv run black .`

Formats the code.

### `uv run ruff check`

Lints the code.

## License

[MIT](https://github.com/remarkablemark/python-microservice-template/blob/master/LICENSE)
