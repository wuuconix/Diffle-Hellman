from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def rsa_genkey() -> tuple:
    """RSA生成公私钥

    RETURNS:
        返回两个参数 第一个是公钥 第二个是私钥
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key, private_key

def rsa_encrypt(data: bytes, public_key: bytes) -> bytes:
    """利用RSA公钥加密"""
    public_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypt_data = cipher_rsa.encrypt(data)
    return encrypt_data

def rsa_decrypt(data: bytes, private_key: bytes) -> bytes:
    """利用RSA私钥解密"""
    private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypt_data = cipher_rsa.decrypt(data)
    return decrypt_data

def test() -> None:
    """测试函数"""
    public_key, private_key = rsa_genkey()
    print(rsa_decrypt(rsa_encrypt(b"wuuconix", public_key), private_key))

# test()