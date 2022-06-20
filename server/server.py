import socket
import json


class Server(object):
    """服务端套接字封装

    Attributes:
        __server: 服务端套接字
    """

    def __init__(self, addr: str, port: int, conn_count: int = 5):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((addr, port))
        self.__server.listen(conn_count)

        print(f'listening: {addr}:{port}')

    def send(self, msg: bytes) -> None:
        """发送数据, 短连接"""
        conn, _ = self.__server.accept()
        conn.send(msg)
        conn.close()

    def recv(self, size: int = 1024) -> bytes:
        """接受数据, 短连接"""
        conn, _ = self.__server.accept()
        msg = conn.recv(size)
        conn.close()
        return msg

    def run(self) -> None:
        """启动DH密钥交换和数据加密传输服务"""
        while True:
            conn, _ = self.__server.accept()
            msg = conn.recv(1024)
            print(json.loads(msg.decode()))
            conn.close()

    def __primitive_root(self, p: int) -> int:
        """求素数p的最小原根"""
        k = (p - 1) // 2
        for i in range(2, p - 1):
            if pow(i, k, p) != 1:
                return i
        return -1


if __name__ == '__main__':
    server = Server('localhost', 23333)
    server.run()
