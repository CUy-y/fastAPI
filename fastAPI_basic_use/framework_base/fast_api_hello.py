from fastapi import FastAPI
import asyncio

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World 666"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

'''
使用uvicorn fast_api_hello:app --reload，
--reload表示代码修改后自动重启服务
'''