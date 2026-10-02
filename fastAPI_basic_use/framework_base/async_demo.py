from fastapi import FastAPI
import asyncio
import time

#创建fastapi实例
app=FastAPI()

@app.get("/async")
async def func_async():
    start =time.time()
    task=[asyncio.sleep(1) for i in range(10)]
    await asyncio.gather(*task)
    end = time.time()
    return {"time":f'{end-start:.2f} seconds'}