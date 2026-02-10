from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck")


@router.get("/")
def healthcheck() -> bool:
    return True
