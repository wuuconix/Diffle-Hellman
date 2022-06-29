from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from traitlets import Bool
import os

KEY_DIRECTORY_PATH = f"{os.path.split(os.path.realpath(__file__))[0]}/CA_KEY"
PUBLIC_KEY_PATH = f"{KEY_DIRECTORY_PATH}/public.pem"

def ca_verify(data: bytes, signature: bytes) -> Bool:
    """RSA签名验证"""
    if (not os.path.exists(PUBLIC_KEY_PATH)):
        raise Exception("项目中找不到CA的公钥 请手动利用gen_key函数生成")
    public_key = RSA.import_key(open(PUBLIC_KEY_PATH).read())
    digest = MD5.new(data)
    try:
        pkcs1_15.new(public_key).verify(digest, signature)
        return True
    except (ValueError, TypeError):
        return False
