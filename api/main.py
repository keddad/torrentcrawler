from fastapi import FastAPI
from datetime import time

app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"Hello {time()}"}
