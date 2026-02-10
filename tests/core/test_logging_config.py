"""Tests for logging configuration."""

import json
import logging
import os
import sys
from collections.abc import Generator
from io import StringIO
from typing import Any

import pytest

from app.core.logging_config import JSONFormatter, get_logger, setup_logging


def create_test_log_record(
    level: int = logging.INFO,
    msg: str = "Test message",
    exc_info: Any = None,
    **extra_fields: object,
) -> logging.LogRecord:
    """Create a test LogRecord with specified parameters.

    Args:
        level: Log level (default: logging.INFO)
        msg: Log message (default: "Test message")
        exc_info: Exception info tuple (default: None)
        **extra_fields: Additional fields to add to the record

    Returns:
        LogRecord instance configured for testing
    """
    record = logging.LogRecord(
        name="test",
        level=level,
        pathname="test.py",
        lineno=10,
        msg=msg,
        args=(),
        exc_info=exc_info,
    )

    # Add extra fields if provided
    if extra_fields:
        record.extra_fields = extra_fields  # type: ignore

    return record


@pytest.fixture
def log_stream() -> Generator[StringIO, None, None]:
    """Create a string stream for capturing log output."""
    stream = StringIO()
    yield stream
    stream.close()


def test_json_formatter_basic() -> None:
    """Test basic JSON formatting of log records."""
    formatter = JSONFormatter()
    record = create_test_log_record()

    result = formatter.format(record)
    log_data = json.loads(result)

    assert log_data["level"] == "INFO"
    assert log_data["logger"] == "test"
    assert log_data["message"] == "Test message"
    assert log_data["module"] == "test"
    assert log_data["line"] == 10
    assert "timestamp" in log_data


def test_json_formatter_with_exception() -> None:
    """Test JSON formatting with exception info."""
    formatter = JSONFormatter()

    try:
        raise ValueError("Test error")
    except ValueError:
        record = create_test_log_record(
            level=logging.ERROR, msg="Error occurred", exc_info=sys.exc_info()
        )

    result = formatter.format(record)
    log_data = json.loads(result)

    assert log_data["level"] == "ERROR"
    assert log_data["message"] == "Error occurred"
    assert "exception" in log_data
    assert log_data["exception"]["type"] == "ValueError"
    assert log_data["exception"]["message"] == "Test error"
    assert "traceback" in log_data["exception"]


def test_setup_logging_default_level() -> None:
    """Test logging setup with default INFO level."""
    os.environ.pop("LOG_LEVEL", None)
    logger = setup_logging()

    assert logger.name == "app"
    assert logger.level == logging.INFO


def test_setup_logging_custom_level() -> None:
    """Test logging setup with custom log level."""
    os.environ["LOG_LEVEL"] = "DEBUG"
    logger = setup_logging()

    assert logger.level == logging.DEBUG

    # Clean up
    os.environ.pop("LOG_LEVEL", None)
    setup_logging()  # Reset to default


def test_get_logger() -> None:
    """Test getting a module-specific logger."""
    logger = get_logger("test_module")

    assert logger.name == "app.test_module"


def test_logger_json_output(log_stream: StringIO) -> None:
    """Test that logger outputs valid JSON."""
    logger = logging.getLogger("test_json")
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info("Test message")

    output = log_stream.getvalue()
    log_data = json.loads(output.strip())

    assert log_data["message"] == "Test message"
    assert log_data["level"] == "INFO"


def test_json_formatter_with_extra_fields() -> None:
    """Test JSON formatting with extra fields."""
    formatter = JSONFormatter()
    record = create_test_log_record(user_id=123, request_id="abc-123")

    result = formatter.format(record)
    log_data = json.loads(result)

    assert log_data["message"] == "Test message"
    assert log_data["user_id"] == 123
    assert log_data["request_id"] == "abc-123"
