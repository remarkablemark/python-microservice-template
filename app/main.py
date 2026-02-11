from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from opentelemetry.instrumentation.fastapi import (  # pyright: ignore[reportMissingTypeStubs]
    FastAPIInstrumentor,
)

from app.api.routes.healthcheck import router as healthcheck_router
from app.api.routes.v1 import router as v1_router
from app.core.database import create_db_and_tables, engine
from app.core.logging_config import get_logger
from app.core.metadata import PROJECT_DESCRIPTION, PROJECT_NAME, PROJECT_VERSION
from app.core.otel import is_otel_enabled, setup_opentelemetry

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler.

    Sets up OpenTelemetry and creates database tables on startup if configured.
    """
    logger.info("Application startup")
    # Startup: Initialize OpenTelemetry if enabled
    setup_opentelemetry()
    # Startup: Create database tables if database is enabled
    if engine is not None:  # pragma: no cover
        logger.info("Database enabled, creating tables")
        create_db_and_tables()
    yield
    # Shutdown: Add cleanup code here if needed
    logger.info("Application shutdown")


app = FastAPI(
    title=PROJECT_NAME,
    version=PROJECT_VERSION,
    description=PROJECT_DESCRIPTION,
    lifespan=lifespan,
)

# Optional: Instrument FastAPI with OpenTelemetry if enabled
if is_otel_enabled():  # pragma: no cover
    logger.info("OpenTelemetry enabled, instrumenting FastAPI")
    FastAPIInstrumentor.instrument_app(app)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Log all HTTP requests."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code}")
    return response


app.include_router(healthcheck_router)
app.include_router(v1_router)
