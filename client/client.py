import socket
import json
from Crypto.Util.number import getRandomInteger
import sys
import os
sys.path.append(f"{os.path.split(os.path.realpath(__file__))[0]}/../utils/")
from AES import aes_encrypt, aes_decrypt
from RSA import rsa_encrypt
from CA import ca_sign, ca_verify

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
        return json.loads(self.__client.recv(3072).decode())

    def run(self) -> None:
        """通过DH密钥传输协议进行数据加密传输"""
        K = self.__key_exchange()
        K = self.__key_format(K)
        print("*******Data Communication*******\n")
        while True:
            plaintext = input("Input Something To Send: ").encode()
            print("")
            ciphertext = aes_encrypt(plaintext, K)
            print(f"Ciphertext: {ciphertext.decode()}\n")
            msg = {
                "status": 3,
                "body": {
                    "msg": ciphertext.decode()
                }
            }
            self.send(msg)
            print("Wating For Server Response...\n")
            msg = self.recv()
            ciphertext = msg["body"]["msg"].encode()
            print(f"Server Ciphertext: {ciphertext.decode()}\n")
            decryptdata = aes_decrypt(ciphertext, K).decode()
            print(f"Plaintext After Decrypt: {decryptdata}\n")

    def __key_exchange(self) -> int:
        """密钥交换过程 返回对称密钥K"""
        print("********DH Key Exchange********")
        input("Type Enter To Send Hello To Server...\n")
        msg = {
            "status": 0,
            "body": {
                "msg": "hello"
            }
        }
        self.send(msg)
        print("Waiting For Server P, g, A...\n")
        res = self.recv()
        p, g, A = res["body"]["p"], res["body"]["g"], res["body"]["A"]
        print(f"Big Prime P: {p}\n")
        print(f"Server Public Key A: {A}\n")
        input("Type Enter To Generate Client Private Key b...\n")
        b = self.__random_integer()
        B = pow(g, b, p)
        print(f"Client Private Key b: {b}\n")
        print(f"Client Public Key B: {B}\n")
        input("Type Enter To Send Client Public Key B To Server...\n")
        msg = {
            "status": 2,
            "body": {
                "B": B
            }
        }
        self.send(msg)
        input("Type Enter To Calcu Final Key K...\n")
        K = pow(A, b, p)
        print(f"Final Key K: {K}\n")
        print("******Done DH Key Exchange******\n")
        return K
    
    def __random_integer(self) -> int:
        """随机得到一个100位的整数"""
        return getRandomInteger(100)

    def __key_format(self, K: int) -> bytes:
        K = str(K) #先将K转化为字符
        K = K[0: 32] #取前32位字符
        K = K.encode() #转变为bytes类型
        return K

if __name__ == '__main__':
    client = Client('localhost', 23333)
    client.run()
