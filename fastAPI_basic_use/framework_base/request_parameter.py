from fastapi import FastAPI
from pydantic import BaseModel


app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


class User(BaseModel):
    username:str
    password:str

class Book(BaseModel):
    book_name:str
    book_price:int

@app.post("/register")
async def register(user:User):
    return user

@app.post("/book")
async def create_book(book:Book):
    return {"书名":book.book_name,"价格":book.book_price}


'''
请求体传递参数不在url中，而是放在请求体中，
使用post body请求方式传递参数

curl -X 'POST' \
  'http://127.0.0.1:8000/register' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "cyy",
  "password": "123"
}'

'''

