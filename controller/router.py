import uuid

import aioredis
from fastapi import FastAPI, Request

app = FastAPI()

redis = aioredis.from_url(
    url="redis://127.0.0.1:6379", encoding="utf-8", decode_responses=True
)


@app.post("/")
async def read_messages(request: Request):
    """Собирается информация из сенсоров, и записывается в redis"""
    body = await request.body()
    await redis.set(str(uuid.uuid1()), body)
