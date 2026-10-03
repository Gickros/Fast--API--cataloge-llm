from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    id: UUID
    title: str
    author: str
    description: str
    price: float
    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    price: float


class BookPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None
