"""В модуле происходит обработка принятых сообщений и выполняется отправка команды манипулятору"""
import asyncio
import json
import logging
import socket
from datetime import datetime
from os import getenv

import aioredis

logging.basicConfig(level=logging.INFO)

redis = aioredis.from_url(
    url=f"redis://{getenv('REDIS_HOST', '127.0.0.1')}:6379",
    encoding="utf-8",
    decode_responses=True,
)
sock = socket.socket()
sock.connect((getenv("MANIPULATOR_HOST", "127.0.0.1"), 9099))
last_processing = None


async def get_status() -> str:
    """Обработка данных с сенсоров"""
    payload = 0
    for key in await redis.keys():
        data = await redis.get(key)
        if not data:
            continue

        message = json.loads(data)
        if not is_outdated(message["datetime"]):
            payload += message["payload"]

    datetime.now()
    return "up" if payload % 2 == 0 else "down"


def is_outdated(raw_datetime) -> bool:
    """Проверка что данные уже участвовали в принятии предыдущего решения"""
    if last_processing is None:
        return False

    data_time = datetime.strptime(raw_datetime, "%Y%m%dT%H%M%S")
    return data_time < last_processing


async def send_control_signal() -> None:
    status = await get_status()
    data = json.dumps(
        {
            "datetime": datetime.now().strftime("%Y%m%dT%H%M%S"),
            "status": status,
        }
    )
    logging.info("Set status " + str(data))
    sock.send(bytes(data, encoding="UTF-8"))


async def main() -> None:
    while True:
        asyncio.create_task(send_control_signal())
        await asyncio.sleep(5)


try:
    asyncio.run(main())

except BaseException as e:
    print(str(e))
    sock.close()
