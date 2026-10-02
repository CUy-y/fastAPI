from fastapi import FastAPI,Path

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World 666"}

@app.get("/book/{id}")
async def get_book(id:int=Path(...,gt=0,lt=101,description="书籍id，取值范围为1-100")):
    return {"id":id,"title":f"这是第{id}本书"}

@app.get("/user/{name}")
async def ger_user(name:str):
    return {"name":name,"msg":f"你好！{name}"}

@app.get("/author/{name}")
async def get_author(name:str=Path(...,min_length=2,max_length=10,description="作者姓名，长度为2-10个字符")):
    return {"msg":f"作者{name}正在学习fastapi"}


@app.get("/news_id/{id}")
async def get_news_id(id:int=Path(...,gt=0,lt=101,description="新闻id，取值范围为1-100")):
    return {"id":id,"title":f"这条新闻的id为{id}"}

@app.get("/news_title/{title}")
async def get_news_title(title:str=Path(...,min_length=2,max_length=10,description="新闻标题，长度为2-10个字符")):
    return {"title":title,"msg":f"这条新闻的标题为{title}"}

'''
大小，长度，表述等等
'''