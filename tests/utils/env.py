"""Environment variable test utilities for managing test environment configuration."""

import os
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def temporary_env_vars(**env_vars: str | None) -> Generator[None, None, None]:
    """
    Context manager that temporarily sets environment variables.

    Args:
        **env_vars: Environment variables to set (name=value). Use None to delete a variable.

    Yields:
        None

    Example:
        with temporary_env_vars(LOG_LEVEL="DEBUG", DATABASE_URL=None):
            # LOG_LEVEL is set to "DEBUG", DATABASE_URL is deleted
            # ... run tests ...
        # Original values are restored
    """
    original_values: dict[str, str | None] = {}

    # Save original values and set new ones
    for key, value in env_vars.items():
        original_values[key] = os.environ.get(key)
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

    try:
        yield
    finally:
        # Restore original values
        for key, original_value in original_values.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value


@contextmanager
def clean_env_vars(*var_names: str) -> Generator[None, None, None]:
    """
    Context manager that temporarily removes specific environment variables.

    Args:
        *var_names: Names of environment variables to remove

    Yields:
        None

    Example:
        with clean_env_vars("OTEL_ENABLED", "OTEL_EXPORTER_OTLP_ENDPOINT"):
            # Both variables are removed
            # ... run tests ...
        # Original values are restored
    """
    original_values: dict[str, str | None] = {}

    # Save original values and remove variables
    for var_name in var_names:
        original_values[var_name] = os.environ.get(var_name)
        os.environ.pop(var_name, None)

    try:
        yield
    finally:
        # Restore original values
        for var_name, original_value in original_values.items():
            if original_value is not None:
                os.environ[var_name] = original_value
