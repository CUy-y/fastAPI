from fastapi import FastAPI,Query

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/news/news_list")
async def get_news_list(
    skip:int=Query(0,description="跳过的条数",lt=100),
    limit:int=10):
    return {"skip":skip,"limit":limit}

@app.get("/book/book_list")
async def get_book_list(
    book_id:int=Query(...,gt=5,lt=256,description="图书id，必须大于5小于256"),
    book_prince:int=Query(...,gt=50,lt=101,description="图书价格，必须大于50小于101")):
    return {"图书价格":f"{book_prince}","图书id":f"{book_id}"}

'''request请求参数传递方式：
 通过url传递参数：/news/news_list?skip=0&limit=10
 可以直接赋值，也可以通过query赋值
'''

