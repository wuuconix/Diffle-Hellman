from Crypto.Cipher import AES
import binascii

def aes_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """aes加密 接受字节类型的明文和密钥 返回hexlify后的bytes密文"""
    cipher = AES.new(key, AES.MODE_GCM, key)
    ciphertext = cipher.encrypt(plaintext)
    return binascii.hexlify(ciphertext)

def aes_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """aes解密 接受hexilify的bytes密文和bytes密钥，返回bytes明文"""
    ciphertext = binascii.unhexlify(ciphertext)
    cipher = AES.new(key, AES.MODE_GCM, key)
    decrptdata = cipher.decrypt(ciphertext)
    return decrptdata

def test() -> None:
    """测试加解密的正确性"""
    ciphertext = aes_encrypt(b"wuuconix", b"wuuconixwuuconix")
    print(ciphertext)
    decrptdata = aes_decrypt(ciphertext, b"wuuconixwuuconix")
    print(decrptdata)

# test()