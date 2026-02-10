"""OpenTelemetry configuration module.

This module provides optional OpenTelemetry instrumentation for the application.
OpenTelemetry is enabled when OTEL_ENABLED environment variable is set to 'true'.
"""

import os

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.core.logging_config import get_logger
from app.core.metadata import PROJECT_NAME

logger = get_logger(__name__)


def is_otel_enabled() -> bool:
    """Check if OpenTelemetry is enabled via environment variable.

    Returns:
        True if OTEL_ENABLED is set to 'true' (case-insensitive), False otherwise.
    """
    return os.getenv("OTEL_ENABLED", "").lower() == "true"


def get_service_name() -> str:
    """Get the service name for OpenTelemetry.

    Returns:
        Service name from OTEL_SERVICE_NAME environment variable,
        defaults to project name from pyproject.toml.
    """
    return os.getenv("OTEL_SERVICE_NAME", PROJECT_NAME)


def get_otel_endpoint() -> str | None:
    """Get the OTLP exporter endpoint.

    Returns:
        OTLP endpoint URL from OTEL_EXPORTER_OTLP_ENDPOINT environment variable,
        or None if not set.
    """
    return os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")


def setup_opentelemetry() -> None:
    """Initialize OpenTelemetry instrumentation.

    Sets up tracing and metrics exporters if OpenTelemetry is enabled.
    This function should be called during application startup.
    """
    if not is_otel_enabled():
        logger.info("OpenTelemetry is disabled")
        return

    endpoint = get_otel_endpoint()
    if not endpoint:
        logger.warning(
            "OTEL_ENABLED is true but OTEL_EXPORTER_OTLP_ENDPOINT is not set, "
            "OpenTelemetry will not export data"
        )
        return

    service_name = get_service_name()
    logger.info(f"Initializing OpenTelemetry for service: {service_name}")

    # Create resource with service name
    resource = Resource.create({"service.name": service_name})

    # Set up tracing
    trace_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=endpoint)
    trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(trace_provider)

    # Set up metrics
    metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=endpoint))
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    logger.info(f"OpenTelemetry initialized with endpoint: {endpoint}")
