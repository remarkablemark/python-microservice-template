"""Project metadata loaded from pyproject.toml."""

from pathlib import Path

from tomllib import load

# Load project metadata from pyproject.toml
_pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
with open(_pyproject_path, "rb") as _f:
    _pyproject = load(_f)
    PROJECT_NAME: str = _pyproject["project"]["name"]
    PROJECT_VERSION: str = _pyproject["project"]["version"]
    PROJECT_DESCRIPTION: str = _pyproject["project"]["description"]
