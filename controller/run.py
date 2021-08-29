"""Запуска API"""
import nest_asyncio  # type: ignore
import uvicorn  # type: ignore

from router import app

nest_asyncio.apply()


if __name__ == "__main__":
    uvicorn.run(app, port=9090, host="127.0.0.1")
