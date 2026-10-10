from pydantic import BaseModel
from decimal import Decimal


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal