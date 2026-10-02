from fastapi import FastAPI
import time

app=FastAPI()

@app.get("/sync")
def func_sync():
    start =time.time()
    for i in range(10):
        time.sleep(1)
    end = time.time()
    return {"time":f'{end-start:.2f} seconds'}