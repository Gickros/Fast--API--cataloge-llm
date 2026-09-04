from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from data import books
from database import SessionLocal
from database import engine
from model import Base, Books
from schemas import Book, BookPatch, BookCreate


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def check_books(db: Session = Depends(get_db)):
    db = db
    books_ = db.query(Books).all()
    return books_


@app.get('/{book_id}')
def check_book(book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.put('/{book_id}')
def rewrite_book(book_id: int, book_data: BookCreate) -> Book:
    for book in books:
        if book.id == book_id:
            book.title = book_data.title
            book.author = book_data.author
            book.description = book_data.description
            book.price = book_data.price
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


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
    new_book = Book(id=len(books) + 1, title=book.title, description=book.description, price=book.price,
                    author=book.author)
    books.append(new_book)
    return new_book
