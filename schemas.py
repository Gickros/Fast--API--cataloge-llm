from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Book(BaseModel):
    id: UUID
    title: str
    author: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)
    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)


class BookPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    author: str | None = None
