import socket
import json
from Crypto.Util.number import getRandomInteger

class Client(object):
    """客户端套接字封装

    Attributes:
        __client: 客户端套接字
    """

    def __init__(self, addr: str, port: int):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((addr, port))

    def send(self, msg: dict) -> None:
        """将传入的json对象转化为字节后发送"""
        self.__client.send(json.dumps(msg).encode())

    def recv(self) -> bytes:
        """将接受的数据进行转化为json格式"""
        return json.loads(self.__client.recv(1024).decode())

    def run(self) -> None:
        """通过DH密钥传输协议进行数据加密传输"""
        K = self.__key_exchange()

    def __key_exchange(self) -> int:
        msg = {
            "status": 0,
            "body": {
                "msg": "hello"
            }
        }
        self.send(msg)
        print("sent hello\n", msg)
        res = self.recv()
        print("got server public key, p and g\n", res)
        p, g, A = res["body"]["p"], res["body"]["g"], res["body"]["A"]
        b = self.__random_integer()
        B = pow(g, b, p)
        msg = {
            "status": 2,
            "body": {
                "B": B
            }
        }
        self.send(msg)
        print("sent client public key\n", msg)
        K = pow(A, b, p)
        print("calculate k: ", K)
        return K
    
    def __random_integer(self) -> int:
        """随机得到一个30位的整数"""
        return getRandomInteger(100)

if __name__ == '__main__':
    client = Client('localhost', 23333)
    client.run()
