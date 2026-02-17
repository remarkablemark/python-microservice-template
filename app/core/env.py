"""Environment variable utilities for type-safe configuration."""

import os


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    Get a boolean environment variable.

    Args:
        key: Environment variable name
        default: Default value if not set (default: False)

    Returns:
        Boolean value (case-insensitive "true" returns True, all else returns False)

    Example:
        debug = get_env_bool("DEBUG", False)
        otel_enabled = get_env_bool("OTEL_ENABLED")
    """
    value = os.getenv(key, "").lower()
    if not value:
        return default
    return value == "true"


def get_env_str(key: str, default: str = "") -> str:
    """
    Get a string environment variable.

    Args:
        key: Environment variable name
        default: Default value if not set (default: empty string)

    Returns:
        String value

    Example:
        service_name = get_env_str("SERVICE_NAME", "my-service")
        log_level = get_env_str("LOG_LEVEL", "INFO")
    """
    return os.getenv(key, default)


def get_env_list(
    key: str, separator: str = ",", default: list[str] | None = None
) -> list[str]:
    """
    Get a list from a delimited environment variable.

    Args:
        key: Environment variable name
        separator: Delimiter to split on (default: ",")
        default: Default value if not set (default: empty list)

    Returns:
        List of stripped string values (empty strings filtered out)

    Example:
        tokens = get_env_list("API_KEYS")
        allowed_hosts = get_env_list("ALLOWED_HOSTS", separator=";")
    """
    if default is None:
        default = []

    value = os.getenv(key, "")
    if not value:
        return default

    return [item.strip() for item in value.split(separator) if item.strip()]
