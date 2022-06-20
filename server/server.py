import socket
import json
from Crypto.Util.number import getPrime, getRandomInteger

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

    def send(self, conn, msg: dict) -> None:
        """将传入的json对象转化为字节后发送"""
        conn.send(json.dumps(msg).encode())

    def recv(self, conn) -> dict:
        """将接受的数据进行转化为json格式"""
        msg = json.loads(conn.recv(1024).decode())
        return msg

    def run(self) -> None:
        """启动DH密钥交换和数据加密传输服务"""
        while True:
            conn, _ = self.__server.accept()
            msg = self.recv(conn)
            if (msg["status"] == 0):
                print("got client hello\n", msg)
            p = self.__prime()
            g = self.__primitive_root(p)
            a = self.__random_integer()
            A = pow(g, a, p)
            msg = {
                "status": 1,
                "body": {
                    "p": p,
                    "g": g,
                    "A": A
                }
            }
            self.send(conn, msg)
            print("sent server public key, p and g\n", msg)
            res = self.recv(conn)
            print("got client public key\n", res)

    def __prime(self) -> int:
        """随机得到一个100位的素数"""
        return getPrime(100)

    def __primitive_root(self, p: int) -> int:
        """求素数p的最小原根"""
        k = (p - 1) // 2
        for i in range(2, p - 1):
            if pow(i, k, p) != 1:
                return i
        return -1

    def __random_integer(self) -> int:
        """随机得到一个30位的整数"""
        return getRandomInteger(100)

if __name__ == '__main__':
    server = Server('localhost', 23333)
    server.run()
