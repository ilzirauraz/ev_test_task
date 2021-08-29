"""Компонент, который принимает сигналы по TCP соединению и выводит их в консоль/логи для демонстрации.
"""
import logging
import socket

logging.basicConfig(level=logging.INFO)


print("running")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 9099))

sock.listen(1)
conn, addr = sock.accept()

try:
    while True:
        data = conn.recv(1024)

        if not data:
            continue

        logging.info("Set status " + data.decode("utf-8"))

except BaseException:
    conn.close()
