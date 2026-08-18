from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    price: float


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    price: float


class BookPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None
