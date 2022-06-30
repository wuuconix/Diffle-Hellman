from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
import os

KEY_DIRECTORY_PATH = f"{os.path.split(os.path.realpath(__file__))[0]}/CA_KEY"
PRIVATE_KEY_PATH = f"{KEY_DIRECTORY_PATH}/private.pem"

def ca_sign(data: bytes) -> bytes:
    """RSA签名"""
    if (not os.path.exists(PRIVATE_KEY_PATH)):
        raise Exception("项目中找不到CA的私钥 请手动利用gen_key函数生成")
    private_key = RSA.import_key(open(PRIVATE_KEY_PATH).read())
    digest = MD5.new(data)
    signature = pkcs1_15.new(private_key).sign(digest)
    return signature