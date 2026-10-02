from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World 666"}

@app.get("/book/{id}")
async def get_book(id:int):
    return {"id":id,"title":f"这是第{id}本书"}

@app.get("/user/{name}")
async def ger_user(name:str):
    return {"name":name,"msg":f"你好！{name}"}

'''
路由就是URL地址和处理函数的映射关系
'''