from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/items")


class Item(BaseModel):
    item_id: int
    q: str | None = None


@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, q: str | None = None) -> Item:
    return Item(item_id=item_id, q=q)
