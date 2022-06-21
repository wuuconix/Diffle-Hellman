from traceback import print_tb
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os

PUBLIC_KEY_PATH = "key/public.pem"
PRIVATE_KEY_PATH = "key/private.pem"
KEY_DIRECTORY_PATH = "key"

def gen_key() -> None:
    """RSA生成公私钥"""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    save(PRIVATE_KEY_PATH, private_key)
    save(PUBLIC_KEY_PATH, public_key)

def rsa_encrypt(data: bytes) -> bytes:
    """利用RSA公钥加密"""
    if (not os.path.exists(PUBLIC_KEY_PATH) or not os.path.exists(PRIVATE_KEY_PATH)):
        if (not os.path.exists(KEY_DIRECTORY_PATH)):
            os.mkdir(KEY_DIRECTORY_PATH)
        gen_key()
    public_key = RSA.import_key(open(PUBLIC_KEY_PATH).read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypt_data = cipher_rsa.encrypt(data)
    return encrypt_data

def rsa_decrypt(data: bytes) -> bytes:
    """利用RSA私钥解密"""
    private_key = RSA.import_key(open(PRIVATE_KEY_PATH).read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypt_data = cipher_rsa.decrypt(data)
    return decrypt_data

def save(path: str, data: bytes) -> None:
    """写文件操作的简单封装"""
    file = open(path, "wb")
    file.write(data)
    file.close()

def test() -> None:
    """测试函数"""
    print(rsa_decrypt(rsa_encrypt(b"wuuconix")))

test()