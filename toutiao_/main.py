from fastapi import FastAPI
from routers import news
 
app = FastAPI()
 
@app.get("/")
async def root():
    return {"message": "Hello World"}
 
 
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
 
# 挂载路由/注册路由
app.include_router(news.router)