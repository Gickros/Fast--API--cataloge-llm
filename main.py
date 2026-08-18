from fastapi import FastAPI, HTTPException

from schemas import BookPatch

app = FastAPI()


@app.get('/books')
def book_list() -> list[BookSchema]:
    return books


@app.get('/books/{book_id}')
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='book not found')


@app.post('/books')
def create_book(book: BookSchema):
    books.append(book)
    return book


@app.delete('/book/{book_id}')
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book.id)
            return {'message': 'Book deleted'}
    raise HTTPException(status_code=404, detail='book not found')


@app.put('/books/{book_id}')
def edit_book(book_id: int, new_book: BookSchema):
    for index, book in enumerate(books):
        if book.id == book_id:
            new_book == book
            return new_book
    raise HTTPException(status_code=404, detail='book not found')


@app.patch('/books/{book_id}')
def patch_book(book_id: int, data: BookPatch):
    for book in books:
        if book.id == book_id:
            if data.title is not None:
                book.title = data.title
            if data.price is not None:
                book.price = data.price
            if data.description is not None:
                book.description = data.description
            if data.author is not None:
                book.author = data.author
            return book
    raise HTTPException(status_code=404, detail='book not found')
