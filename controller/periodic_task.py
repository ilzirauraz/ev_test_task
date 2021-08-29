"""В модуле происходит обработка принятых сообщений и выполняется отправка команды манипулятору"""
import asyncio
import json
import socket
from datetime import datetime, timedelta

import aioredis


redis = aioredis.from_url(
    url="redis://127.0.0.1:6379", encoding="utf-8", decode_responses=True
)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9099))


async def get_status():
    """Обработка данных с сенсоров"""
    payload = 0
    keys = await redis.keys()
    for key in keys:
        data = await redis.get(key)
        if not data:
            continue
        message = json.loads(data)
        if not is_outdated(message["datetime"]):
            payload += message["payload"]
    if payload % 2:
        return "up"
    return "down"


def is_outdated(time):
    """Проверка что данные уже участвовали в принятии предыдущего решения"""
    data_time = datetime.strptime(time, "%Y%m%dT%H%M%S")
    five_seconds_ago = datetime.now() - timedelta(seconds=5)
    return data_time < five_seconds_ago


async def send_control_signal() -> None:
    status = await get_status()
    data = json.dumps(
        {
            "status": status,
            "datetime": datetime.now().strftime("%Y%m%dT%H%M%S"),
        }
    )
    print(data)
    sock.send(bytes(data, encoding="UTF-8"))


async def main():
    while True:
        print("start iteration")
        asyncio.create_task(send_control_signal())
        await asyncio.sleep(5)


try:
    asyncio.run(main())

except BaseException as e:
    print(str(e))
    sock.close()
