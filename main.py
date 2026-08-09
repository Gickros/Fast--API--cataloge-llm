from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
app = FastAPI()



class  BookSchema(BaseModel):
    id : int
    title : str
    description : str
    price : int
    author : str

books: list[BookSchema]= [] 

@app.get('/books')
def book_list(): --> list[BookSchema]:
    return books
@app.get('/books/{book_id}')
def get_book(book_id:int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404,detail='book not found')


@app.post('/books')
def create_book(book:BookSchema):
    books.append(book)
    return book
@app.delete('/book/{book_id}')
def delete_book(book_id: int):
    for book in books:
        if book.id ==book_id:
            books.remove(book.id)
            return {'message':'Book deleted'}
    raise HTTPException(status_code=404,detail='book not found')
@app.put('/books/{book_id}')
def rewrite_book(book_id):
    for  index,book in books:
        if book.id == book_id:
            
