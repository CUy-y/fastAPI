from fastapi import FastAPI
from pydantic import BaseModel,Field


app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


class User(BaseModel):
    username:str
    password:str

class Book(BaseModel):
    book_name:str=Field(...,gt=5,lt=256,description="图书名称，必须大于5小于256")
    book_price:int=Field(...,gt=50,lt=101,description="图书价格，必须大于50小于101")

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

