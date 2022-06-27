from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from traitlets import Bool
import os

KEY_DIRECTORY_PATH = f"{os.path.split(os.path.realpath(__file__))[0]}/../utils/CA_KEY"
PUBLIC_KEY_PATH = f"{KEY_DIRECTORY_PATH}/public.pem"
PRIVATE_KEY_PATH = f"{KEY_DIRECTORY_PATH}/private.pem"

def gen_key():
    """生成RSA公私钥 存储在public.pem和private.pem 并传送给client公钥
       项目中已经生成了一组CA的公私钥，请保持不变
    """
    key = RSA.generate(1024)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    save(PRIVATE_KEY_PATH, private_key)
    save(PUBLIC_KEY_PATH, public_key)

def ca_sign(data: bytes) -> bytes:
    """RSA签名"""
    if (not os.path.exists(PUBLIC_KEY_PATH) or not os.path.exists(PRIVATE_KEY_PATH)):
        raise Exception("项目中找不到CA的公私钥匙 请手动利用gen_key函数生成")
    private_key = RSA.import_key(open(PRIVATE_KEY_PATH).read())
    digest = MD5.new(data)
    signature = pkcs1_15.new(private_key).sign(digest)
    return signature

def ca_verify(data: bytes, signature: bytes) -> Bool:
    """RSA签名验证"""
    public_key = RSA.import_key(open(PUBLIC_KEY_PATH).read())
    digest = MD5.new(data)
    try:
        pkcs1_15.new(public_key).verify(digest, signature)
        return True
    except (ValueError, TypeError):
        return False

def save(path: str, data: bytes):
    """写文件操作的简单封装"""
    file = open(path, "wb")
    file.write(data)
    file.close()

def test() -> None:
    """测试函数"""
    print(ca_verify(b"wuuconix", ca_sign(b"wuuconix")))

if __name__ == "__main__":
    gen_key()
    test()