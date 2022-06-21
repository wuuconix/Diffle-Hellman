from Crypto.PublicKey import RSA
import os
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from traitlets import Bool

class CA(object):
    """模拟CA
    """

    def __init__(self):
        """构造函数 检测目录下有无公私钥 没有则生成"""
        if not (os.path.exists("public.pem") and os.path.exists("private.pem")):
            self.__gen_key()
        self.public_key = RSA.import_key(open("public.pem").read())
        self.private_key = RSA.import_key(open("private.pem").read())

    def __gen_key(self):
        """生成RSA公私钥 存储在public.pem和private.pem 并传送给client公钥"""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        self.__save("private.pem", private_key)
        self.__save("public.pem", public_key)
        self.__save("../client/ca-public.pem", public_key)

    def sign(self, data: bytes) -> bytes:
        """RSA签名"""
        key = self.private_key
        digest = MD5.new(data)
        signature = pkcs1_15.new(key).sign(digest)
        return signature

    def verify(self, data: bytes, signature: bytes) -> Bool:
        """RSA签名验证"""
        key = self.public_key
        digest = MD5.new(data)
        try:
            pkcs1_15.new(key).verify(digest, signature)
            return True
        except (ValueError, TypeError):
            return False

    def __save(self, path: str, data: bytes):
        file = open(path, "wb")
        file.write(data)
        file.close()
    
if __name__ == '__main__':
    ca = CA()
    # print(ca.verify(b"wuuconix", ca.sign(b"wuuconix")))
