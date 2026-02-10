from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

from app.auth import is_auth_enabled
from app.database import create_db_and_tables, engine
from app.healthcheck import router as healthcheck_router
from app.items import router as items_router
from app.logging_config import get_logger
from app.protected import router as protected_router
from app.users import router as users_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler.

    Creates database tables on startup if database is configured.
    """
    logger.info("Application startup")
    # Startup: Create database tables if database is enabled
    if engine is not None:  # pragma: no cover
        logger.info("Database enabled, creating tables")
        create_db_and_tables()
    yield
    # Shutdown: Add cleanup code here if needed
    logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)


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
app.include_router(items_router)

# Optional: Include protected routers if auth is enabled
if is_auth_enabled():  # pragma: no cover
    logger.info("Authentication enabled, including protected routes")
    app.include_router(protected_router)

# Optional: Include database-dependent routers if database is configured
if engine is not None:  # pragma: no cover
    logger.info("Database configured, including user routes")
    app.include_router(users_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint."""
    logger.debug("Root endpoint called")
    return {"Hello": "World"}
