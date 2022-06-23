import socket
import json
from Crypto.Util.number import getPrime, getRandomInteger
import sys
import os
from binascii import hexlify, unhexlify

sys.path.append(f"{os.path.split(os.path.realpath(__file__))[0]}/../utils/")
from AES import aes_encrypt, aes_decrypt
from RSA import rsa_decrypt, rsa_genkey
from CA import ca_sign

COMUNICATION_LENGTH = 1400

class Server(object):
    """服务端套接字封装

    Attributes:
        __server: 服务端套接字
        __public_key: RSA公钥
        __private_key: RSA私钥
    """

    def __init__(self, addr: str, port: int, conn_count: int = 1):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__server.bind((addr, port))
        self.__server.listen(conn_count)
        self.__public_key, self.__private_key = rsa_genkey()
        print(f'Listening: {addr}:{port}\n')
        print(f"RSA Pulic Key:\n{self.__public_key.decode()}\n")

    def send(self, conn, msg: dict) -> None:
        """将传入的json对象转化为字节后发送"""
        conn.send(json.dumps(msg).encode())

    def recv(self, conn) -> dict:
        """将接受的数据进行转化为json格式"""
        msg = json.loads(conn.recv(COMUNICATION_LENGTH).decode())
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
        input("Type Enter To Generate Big Prime p, Primitve Root g, Server Private Key a and CA Sign\n")
        p = self.__prime()
        g = self.__primitive_root(p)
        a = self.__random_integer()
        A = pow(g, a, p)
        sign = ca_sign(self.__public_key)
        sign = hexlify(sign).decode()
        print(f"Big Prime P: {p}\n")
        print(f"Server Private Key a: {a}\n")
        print(f"Server Public Key A: {A}\n")
        print(f"CA Sign: {sign}\n")
        input("Type Enter To Send Server Public Key A To Client And Waiting For Client Public Key...\n")
        msg = {
            "status": 1,
            "body": {
                "p": p,
                "g": g,
                "A": A,
                "pk": self.__public_key.decode(),
                "sign": sign
            }
        }
        self.send(conn, msg)
        res = self.recv(conn)
        B = res["body"]["B"]
        print(f"Client Public Key B (Encryped): {B}\n")
        input("Type Enter To Decryped B...\n")
        B = int(rsa_decrypt(unhexlify(B.encode()), self.__private_key).decode())
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
        K = K[0: 32] #取前32位字符
        K = K.encode() #转变为bytes类型
        return K

if __name__ == '__main__':
    server = Server('localhost', 23333)
    server.run()
