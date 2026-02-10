"""Tests for OpenTelemetry configuration."""

import os
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from app.core.otel import (
    get_otel_endpoint,
    get_service_name,
    is_otel_enabled,
    setup_opentelemetry,
)


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Clean up OpenTelemetry environment variables."""
    otel_vars = [
        "OTEL_ENABLED",
        "OTEL_SERVICE_NAME",
        "OTEL_EXPORTER_OTLP_ENDPOINT",
    ]
    original_values = {var: os.getenv(var) for var in otel_vars}

    # Clear all OTEL env vars
    for var in otel_vars:
        if var in os.environ:
            del os.environ[var]

    yield

    # Restore original values
    for var, value in original_values.items():
        if value is not None:
            os.environ[var] = value
        elif var in os.environ:
            del os.environ[var]


def test_is_otel_enabled_default(clean_env: None) -> None:  # noqa: ARG001
    """Test that OpenTelemetry is disabled by default."""
    assert is_otel_enabled() is False


def test_is_otel_enabled_true(clean_env: None) -> None:  # noqa: ARG001
    """Test that OpenTelemetry is enabled when env var is 'true'."""
    os.environ["OTEL_ENABLED"] = "true"
    assert is_otel_enabled() is True


def test_is_otel_enabled_true_case_insensitive(clean_env: None) -> None:  # noqa: ARG001
    """Test that OTEL_ENABLED is case-insensitive."""
    os.environ["OTEL_ENABLED"] = "TRUE"
    assert is_otel_enabled() is True

    os.environ["OTEL_ENABLED"] = "True"
    assert is_otel_enabled() is True


def test_is_otel_enabled_false(clean_env: None) -> None:  # noqa: ARG001
    """Test that OpenTelemetry is disabled when env var is not 'true'."""
    os.environ["OTEL_ENABLED"] = "false"
    assert is_otel_enabled() is False

    os.environ["OTEL_ENABLED"] = "1"
    assert is_otel_enabled() is False

    os.environ["OTEL_ENABLED"] = "yes"
    assert is_otel_enabled() is False


def test_get_service_name_default(clean_env: None) -> None:  # noqa: ARG001
    """Test that service name defaults to 'python-microservice-template'."""
    assert get_service_name() == "python-microservice-template"


def test_get_service_name_custom(clean_env: None) -> None:  # noqa: ARG001
    """Test that custom service name is used when env var is set."""
    os.environ["OTEL_SERVICE_NAME"] = "my-custom-service"
    assert get_service_name() == "my-custom-service"


def test_get_otel_endpoint_default(clean_env: None) -> None:  # noqa: ARG001
    """Test that OTLP endpoint is None by default."""
    assert get_otel_endpoint() is None


def test_get_otel_endpoint_custom(clean_env: None) -> None:  # noqa: ARG001
    """Test that custom OTLP endpoint is used when env var is set."""
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4317"
    assert get_otel_endpoint() == "http://localhost:4317"


@patch("app.core.otel.logger")
def test_setup_opentelemetry_disabled(
    mock_logger: MagicMock,
    clean_env: None,  # noqa: ARG001
) -> None:
    """Test that setup does nothing when OpenTelemetry is disabled."""
    setup_opentelemetry()
    mock_logger.info.assert_called_once_with("OpenTelemetry is disabled")


@patch("app.core.otel.logger")
def test_setup_opentelemetry_no_endpoint(
    mock_logger: MagicMock,
    clean_env: None,  # noqa: ARG001
) -> None:
    """Test that setup warns when enabled but no endpoint is configured."""
    os.environ["OTEL_ENABLED"] = "true"
    setup_opentelemetry()

    assert mock_logger.warning.call_count == 1
    warning_msg = mock_logger.warning.call_args[0][0]
    assert "OTEL_EXPORTER_OTLP_ENDPOINT is not set" in warning_msg


@patch("app.core.otel.metrics.set_meter_provider")
@patch("app.core.otel.trace.set_tracer_provider")
@patch("app.core.otel.logger")
def test_setup_opentelemetry_with_endpoint(
    mock_logger: MagicMock,
    mock_set_tracer: MagicMock,
    mock_set_meter: MagicMock,
    clean_env: None,  # noqa: ARG001
) -> None:
    """Test that OpenTelemetry is properly initialized with endpoint."""
    os.environ["OTEL_ENABLED"] = "true"
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4317"
    os.environ["OTEL_SERVICE_NAME"] = "test-service"

    setup_opentelemetry()

    # Verify logger calls
    assert mock_logger.info.call_count == 2
    assert "Initializing OpenTelemetry for service: test-service" in str(
        mock_logger.info.call_args_list[0]
    )
    assert "OpenTelemetry initialized with endpoint: http://localhost:4317" in str(
        mock_logger.info.call_args_list[1]
    )

    # Verify providers were set
    mock_set_tracer.assert_called_once()
    mock_set_meter.assert_called_once()


@patch("app.core.otel.metrics.set_meter_provider")
@patch("app.core.otel.trace.set_tracer_provider")
@patch("app.core.otel.logger")
def test_setup_opentelemetry_default_service_name(
    mock_logger: MagicMock,
    _mock_set_tracer: MagicMock,
    _mock_set_meter: MagicMock,
    clean_env: None,  # noqa: ARG001
) -> None:
    """Test that OpenTelemetry uses default service name when not specified."""
    os.environ["OTEL_ENABLED"] = "true"
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4317"

    setup_opentelemetry()

    # Verify default service name is used
    assert (
        "Initializing OpenTelemetry for service: python-microservice-template"
        in str(mock_logger.info.call_args_list[0])
    )
