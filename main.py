from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from uuid import uuid4, UUID

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_engine
from model import Base
from model import Books
from schemas import Book, BookPatch, BookCreate


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession() as db:
        yield db


@app.get('/', response_model=Book)
async def check_books(db: AsyncSession = Depends(get_db_async)):
    result = await db.execute(select(Books))
    return result.scalars().all()


@app.get('/{book_id}', response_model=Book)
async def check_book(book_id: UUID, db: AsyncSession = Depends(get_db_async)) -> Book:
    result = await db.execute(select(Books)).where(Books.id == book_id).all()
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result.scalar_one_or_none()


@app.put('/{book_id}', response_model=Book, )
async def rewrite_book(book_id: UUID, db: AsyncSession = Depends(get_db_async)) -> Book:
    book = await db.execute(select(Book)).where(Book.id == book_id)
    if Book.title is not None:
        Book.title = book.title
    if Book.author is not None:
        Book.author = book.author
    if Book.description is not None:
        Book.description = book.description
    if Book.price is not None:
        Book.price = book.price

    db.commit()
    db.refresh(book)
    return book.scalar_one_or_none()


@app.delete('/{book_id}')
def delete_book(book_id: int) -> str:
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return 'book deleted'
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch('/{book_id}')
def patch_book(book_id: int, book_data: BookPatch) -> Book:
    for book in books:
        if book.id == book_id:
            if book_data.title is not None:
                book.title = book_data.title
            if book_data.author is not None:
                book.author = book_data.author
            if book_data.description is not None:
                book.description = book_data.description
            if book_data.price is not None:
                book.price = book_data.price
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.post('/create/')
def create_book(book: BookCreate) -> Book:
    new_book = Book(id=uuid4(), title=book.title, description=book.description, price=book.price,
                    author=book.author)
    books.append(new_book)
    return new_book
