"""Компонент, генерирующий данные, на основе которых контроллер принимает решение.
Всего 8 сенсоров, каждый генерирует 300 сообщений в секунду,
сообщения равномерно распределены по секунде и отправляются раздельно (один запрос на одно сообщение).
Алгоритм генерации данных на усмотрение.
"""
import random
from asyncio import create_task, run, sleep
from datetime import datetime
from typing import Any, Dict, List

import requests

RPS = 300


async def make_request() -> None:
    """Генерирует сообщения"""
    message = {
        "datetime": datetime.now().strftime("%Y%m%dT%H%M%S"),
        "payload": random.randint(0, 10),
    }
    requests.post("http://127.0.0.1:9090/", json=message)


async def start():
    """Отправляет сообщения. 1 запрос на 1 сообщение"""
    while True:
        create_task(make_request())
        await sleep(1 / RPS)


run(start())
