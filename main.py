from contextlib import asynccontextmanager
from uuid import uuid4, UUID

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_async
from exceptions import get_or_404
from model import Books
from schemas import Book, BookCreate, BookPatch


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/', response_model=list[Book])
async def check_books(db: AsyncSession = Depends(get_db_async)):
    result = await db.execute(select(Books).limit(10).offset(0))
    book = result.scalars().all()
    return book


@app.get('/{book_id}', response_model=Book)
async def check_book(book_id: UUID, db: AsyncSession = Depends(get_db_async)) -> Books:
    result = await db.execute(select(Books).where(Books.id == book_id))
    book = get_or_404(result.scalar_one_or_none())
    return book


@app.put('/{book_id}', response_model=Book)
async def rewrite_book(book_id: UUID, book_data: BookCreate, db: AsyncSession = Depends(get_db_async)) -> Books:
    result = await db.execute(select(Books).where(Books.id == book_id))
    book = get_or_404(result.scalar_one_or_none())
    book.title = book_data.title
    book.description = book_data.description
    book.price = book_data.price
    book.author = book_data.author

    await db.commit()
    await db.refresh(book)
    return book


@app.delete('/{book_id}')
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db_async)) -> str:
    result = await db.execute(select(Books).where(Books.id == book_id))
    book = get_or_404(result.scalar_one_or_none())
    await db.delete(book)
    await db.commit()
    return 'Book deleted'


@app.patch('/{book_id}', response_model=Book)
async def patch_book(book_id: UUID, book_data: BookPatch, db: AsyncSession = Depends(get_db_async)) -> Books:
    result = await db.execute(select(Books).where(Books.id == book_id))
    book = get_or_404(result.scalar_one_or_none())
    if book_data.title is not None:
        book.title = book_data.title
    if book_data.description is not None:
        book.description = book_data.description
    if book_data.price is not None:
        book.price = book_data.price
    if book_data.author is not None:
        book.author = book_data.author
    await db.commit()
    await db.refresh(book)
    return book


@app.post('/create/', response_model=Book, status_code=201)
async def create_book(book_data: BookCreate, db: AsyncSession = Depends(get_db_async)) -> Books:
    book = Books(id=uuid4(), title=book_data.title, author=book_data.author, price=book_data.price,
                 description=book_data.description)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book
