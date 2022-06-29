from Crypto.PublicKey import RSA
import os

BASE_PATH = f"{os.path.split(os.path.realpath(__file__))[0]}"
PUBLIC_KEY_PATH = f"{BASE_PATH}/client/CA_KEY/public.pem"
PRIVATE_KEY_PATH = f"{BASE_PATH}/server/CA_KEY/private.pem"

def gen_key():
    """生成RSA公私钥 存储在public.pem和private.pem下
    并将私钥存储在server/CA_KEY下，公钥则存储在client/CA_KEY下
    """
    key = RSA.generate(1024)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    save(PRIVATE_KEY_PATH, private_key)
    save(PUBLIC_KEY_PATH, public_key)

def save(path: str, data: bytes):
    """写文件操作的简单封装"""
    with open(path, "wb") as file:
        file.write(data)

if __name__ == "__main__":
    #运行此文件生成CA的公私钥，并分别存于server下和client下
    gen_key()