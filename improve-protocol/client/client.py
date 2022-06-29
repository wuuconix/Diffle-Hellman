import socket
import json
from Crypto.Util.number import getRandomInteger
import sys

from AES import aes_encrypt, aes_decrypt
from RSA import rsa_encrypt
from CA import ca_verify
from binascii import hexlify, unhexlify

COMUNICATION_LENGTH = 1400

class Client(object):
    """客户端套接字封装

    Attributes:
        __client: 客户端套接字
    """

    def __init__(self, addr: str, port: int):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__client.connect((addr, port))

    def send(self, msg: dict) -> None:
        """将传入的json对象转化为字节后发送
           利用b'\xff'填充至 COMUNICATION_LENGTH位 的二进制个数
        """
        msg_bytes = json.dumps(msg).encode()
        msg_bytes = msg_bytes + (COMUNICATION_LENGTH - len(msg_bytes)) * b'\xff'
        self.__client.send(msg_bytes)

    def recv(self) -> bytes:
        """将接受的数据进行转化为json格式
           利用decode('ascii', 'ignore')忽略最后的填充b'\xff'
        """
        return json.loads(self.__client.recv(COMUNICATION_LENGTH).decode('ascii', "ignore"))

    def run(self) -> None:
        """通过DH密钥传输协议进行数据加密传输"""
        K = self.__key_exchange()
        K = self.__key_format(K)
        print("*******Data Communication*******\n")
        while True:
            plaintext = input("Input Something To Send: ").encode()
            print()
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
        print("Waiting For Server P, g, A, pk, sign...\n")
        res = self.recv()
        p, g, A = res["body"]["p"], res["body"]["g"], res["body"]["A"]
        pk, sign = res["body"]["pk"], res["body"]["sign"]
        print(f"Big Prime P: {p}\n")
        print(f"Server Public Key A: {A}\n")
        print(f"Server RSA Public Key pk: \n{pk}\n")
        print(f"CA sign: {sign}\n")
        input("Type Enter To Verify Sign...\n")
        pk = pk.encode()
        sign =  unhexlify(sign.encode())
        if (ca_verify(pk, sign)):
            print("Sign Verified!\n")
        else:
            print("Sign UnVerified! Exit!\n")
            exit()
        input("Type Enter To Generate Client Private Key b And Encrypt it...\n")
        b = self.__random_integer()
        B = pow(g, b, p)
        print(str(B).encode(), len(str(B).encode()))
        encrypt_B = hexlify(rsa_encrypt(str(B).encode(), pk)).decode()
        print(f"Client Private Key b: {b}\n")
        print(f"Client Public Key B: {B}\n")
        print(f"Client Public Key B (Encryped): {encrypt_B}\n")
        input("Type Enter To Send Client Public Key B To Server...\n")
        msg = {
            "status": 2,
            "body": {
                "B": encrypt_B
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
    if len(sys.argv) != 3:
        print("Usage: python3 server.py addr port")
        exit(0)
    addr, port = sys.argv[1], sys.argv[2]
    client = Client(addr, int(port))
    client.run()

