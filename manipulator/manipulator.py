"""Компонент, который принимает сигналы по TCP соединению и выводит их в консоль/логи для демонстрации.
"""
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 9099))

sock.listen(1)
conn, addr = sock.accept()

try:
    while True:
        data = conn.recv(1024)
        if not data:
            continue
        print(data)

except BaseException:
    conn.close()
