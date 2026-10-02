from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World 666"}

@app.get("/hello")
async def say_hello():
    return {"msg":"你好！"}

@app.get("/user/hello")
async def user_hello():
    return {"msg":"我正在学习fastapi！"}
'''
路由就是URL地址和处理函数的映射关系
'''