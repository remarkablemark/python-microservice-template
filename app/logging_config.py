"""Logging configuration for the application.

Provides standardized JSON logging setup with configurable log levels.
"""

import json
import logging
import os
import sys
import traceback
from datetime import datetime, timezone
from typing import Any


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record to format.

        Returns:
            JSON-formatted log string.
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info),
            }

        # Add extra fields from record
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)  # type: ignore

        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """Configure and return the application logger.

    Log level can be controlled via LOG_LEVEL environment variable.
    Defaults to INFO.

    Returns:
        Configured logger instance.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Create JSON formatter
    json_formatter = JSONFormatter()

    # Configure handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(json_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Get application logger
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.

    Args:
        name: Logger name, typically __name__ of the calling module.

    Returns:
        Logger instance.
    """
    return logging.getLogger(f"app.{name}")


# Create the main application logger
logger = setup_logging()
