from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables, engine
from app.healthcheck import router as healthcheck_router
from app.items import router as items_router
from app.users import router as users_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler.

    Creates database tables on startup if database is configured.
    """
    # Startup: Create database tables if database is enabled
    if engine is not None:
        create_db_and_tables()
    yield
    # Shutdown: Add cleanup code here if needed


app = FastAPI(lifespan=lifespan)

app.include_router(healthcheck_router)
app.include_router(items_router)

# Optional: Include database-dependent routers if database is configured
if engine is not None:
    app.include_router(users_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
