import socket


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
        conn, addr = self.__server.accept()
        msg = conn.recv(size)
        conn.close()
        return msg, addr


if __name__ == '__main__':
    server = Server('localhost', 23333)
    while True:
        msg, addr = server.recv()
        print('----------')
        print(f'client: {addr[0]}:{addr[1]}\nmessage: {msg.decode()}')
