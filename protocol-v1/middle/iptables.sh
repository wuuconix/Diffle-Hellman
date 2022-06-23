#!/bin/sh

iptables -A FORWARD -p tcp --tcp-flags ALL PSH,ACK -j NFQUEUE --queue-num 0
iptables -A OUTPUT -p icmp --icmp-type redirect -j DROP
