from pydoc import cli
import socket


class Client:
    def __init__(self, addr, port):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((addr, port))

    def send_msg(self, msg):
        self.__client.send(msg)

    def recv_msg(self, size=1024):
        return self.__client.recv(1024)

    def __del__(self):
        self.__client.close()


if __name__ == '__main__':
    client = Client('localhost', 23333)
    client.send_msg('hello'.encode())
