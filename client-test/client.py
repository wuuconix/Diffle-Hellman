import socket


class Client(object):
    """客户端套接字封装
    Attributes:
        __client: 客户端套接字
    """

    def __init__(self, addr: str, port: int):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((addr, port))

    def send(self, msg: bytes) -> None:
        """发送数据"""
        self.__client.send(msg)

    def recv(self, size: int = 1024) -> bytes:
        """接受数据"""
        return self.__client.recv(size)

    def __del__(self):
        self.__client.close()


if __name__ == '__main__':
    client = Client('localhost', 23333)
    msg = 'Hello'.encode()
    client.send(msg)
