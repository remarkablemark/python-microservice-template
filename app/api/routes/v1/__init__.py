"""V1 API routes."""

from fastapi import APIRouter

from app.api.routes.v1.items import router as items_router
from app.api.routes.v1.protected import router as protected_router
from app.api.routes.v1.users import router as users_router
from app.core.auth import is_auth_enabled
from app.core.database import engine
from app.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/v1")

router.include_router(items_router)

# Optional: Include protected routers if auth is enabled
if is_auth_enabled():  # pragma: no cover
    logger.info("Authentication enabled, including protected routes")
    router.include_router(protected_router)

# Optional: Include database-dependent routers if database is configured
if engine is not None:  # pragma: no cover
    logger.info("Database configured, including user routes")
    router.include_router(users_router)
