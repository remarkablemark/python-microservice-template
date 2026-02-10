from fastapi import FastAPI

from app.healthcheck import router as healthcheck_router
from app.items import router as items_router

app = FastAPI()

app.include_router(healthcheck_router)
app.include_router(items_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
