from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def healthcheck() -> dict[str, str]:
    """Healthcheck endpoint."""
    return {"status": "ok"}
