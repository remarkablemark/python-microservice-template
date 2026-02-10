# fastapi-template

[![codecov](https://codecov.io/gh/remarkablemark/fastapi-template/graph/badge.svg?token=ldtrSznCY4)](https://codecov.io/gh/remarkablemark/fastapi-template)
[![test](https://github.com/remarkablemark/fastapi-template/actions/workflows/test.yml/badge.svg)](https://github.com/remarkablemark/fastapi-template/actions/workflows/test.yml)
[![lint](https://github.com/remarkablemark/fastapi-template/actions/workflows/lint.yml/badge.svg)](https://github.com/remarkablemark/fastapi-template/actions/workflows/lint.yml)

⚡ [FastAPI](https://fastapi.tiangolo.com/) template inspired by [Full Stack FastAPI Template](https://fastapi.tiangolo.com/project-generation/).

## Prerequisites

[uv](https://docs.astral.sh/uv/#installation):

```sh
brew install uv
```

## Install

Clone the repository:

```sh
git clone https://github.com/remarkablemark/fastapi-template.git
cd fastapi-template
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

### `uv run fastapi run`

Runs the app in production mode.

### `uv run pre-commit install`

Installs the pre-commit script.

### `uv run black .`

Formats the code.

### `uv run ruff check`

Lints the code.

## License

[MIT](https://github.com/remarkablemark/fastapi-template/blob/master/LICENSE)
