import socket
import json
from Crypto.Util.number import getPrime, getRandomInteger
import sys
from AES import aes_decrypt, aes_encrypt

COMUNICATION_LENGTH = 1400

class Server(object):
    """服务端套接字封装

    Attributes:
        __server: 服务端套接字
    """

    def __init__(self, addr: str, port: int, conn_count: int = 1):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((addr, port))
        self.__server.listen(conn_count)

        print(f'Listening: {addr}:{port}')

    def send(self, conn, msg: dict) -> None:
        """将传入的json对象转化为字节后发送
           利用b'\xff'填充至 COMUNICATION_LENGTH位 的二进制个数
        """
        msg_bytes = json.dumps(msg).encode()
        msg_bytes = msg_bytes + (COMUNICATION_LENGTH - len(msg_bytes)) * b'\xff'
        conn.send(msg_bytes)

    def recv(self, conn) -> dict:
        """将接受的数据进行转化为json格式
           利用decode('ascii', 'ignore')忽略最后的填充b'\xff'
        """
        msg = json.loads(conn.recv(COMUNICATION_LENGTH).decode('ascii', "ignore"))
        return msg

    def run(self) -> None:
        """启动DH密钥交换和数据加密传输服务"""
        conn, _ = self.__server.accept()
        K = self.__key_exchange(conn)
        K = self.__key_format(K)
        print("*******Data Communication*******\n")
        while True: #不断和客户端通信
            print("Wating For Client Msg...\n")
            msg = self.recv(conn)
            ciphertext = msg["body"]["msg"].encode()
            print(f"Client Ciphertext: {ciphertext.decode()}\n")
            decryptdata = aes_decrypt(ciphertext, K).decode()
            print(f"Plaintext After Decrypt: {decryptdata}\n")
            plaintext = input("Input Something To Respond: ").encode()
            print("")
            ciphertext = aes_encrypt(plaintext, K)
            print(f"Ciphertext: {ciphertext.decode()}\n")
            msg = {
                "status": 3,
                "body": {
                    "msg": ciphertext.decode()
                }
            }
            self.send(conn, msg)

    def __key_exchange(self, conn) -> int:
        """密钥交换过程 返回对称密钥K"""
        print("********DH Key Exchange********")
        msg = self.recv(conn)
        if (msg["status"] == 0):
            print("Got Client Hello\n")
        input("Type Enter To Generate Big Prime p, Primitve Root g and Server Private Key a...\n")
        p = self.__prime()
        g = self.__primitive_root(p)
        a = self.__random_integer()
        A = pow(g, a, p)
        print(f"Big Prime P: {p}\n")
        print(f"Server Private Key a: {a}\n")
        print(f"Server Public Key A: {A}\n")
        input("Type Enter To Send Server Public Key A To Client And Waiting For Client Public Key...\n")
        msg = {
            "status": 1,
            "body": {
                "p": p,
                "g": g,
                "A": A
            }
        }
        self.send(conn, msg)
        res = self.recv(conn)
        B = res["body"]["B"]
        print(f"Client Public Key B: {B}\n")
        input("Type Enter To Calcu Final Key K...\n")
        K = pow(B, a, p)
        print(f"Final Key K: {K}\n" )
        print("******Done DH Key Exchange******\n")
        return K

    def __prime(self) -> int:
        """随机得到一个300位的素数"""
        return getPrime(300)

    def __primitive_root(self, p: int) -> int:
        """求素数p的最小原根"""
        k = (p - 1) // 2
        for i in range(2, p - 1):
            if pow(i, k, p) != 1:
                return i
        return -1

    def __random_integer(self) -> int:
        """随机得到一个100位的整数"""
        return getRandomInteger(100)

    def __key_format(self, K: int) -> bytes:
        K = str(K) #先将K转化为字符
        K = K[0: 16] #取前16位字符
        K = K.encode() #转变为bytes类型
        return K

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 server.py addr port")
        exit(0)
    addr, port = sys.argv[1], sys.argv[2]
    server = Server(addr, int(port))
    server.run()
