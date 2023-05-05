import pcapy
from struct import *

# Open the network interface in promiscuous mode
capture = pcapy.open_live("enp0s3", 65536, 1, 0)

# Loop through incoming packets
while True:
    (header, packet) = capture.next()
    
    # Extract the Ethernet header fields
    eth_header = unpack("!6s6sH", packet[:14])
    eth_protocol = socket.ntohs(eth_header[2])
    
    # Check if the packet is TCP or UDP
    if eth_protocol == 8:  # IPv4
        ip_header = unpack("!BBHHHBBH4s4s", packet[14:34])
        protocol = ip_header[6]
        if protocol == 6:
            print("TCP packet")
        elif protocol == 17:
            print("UDP packet")
    elif eth_protocol == 1544:  # IPv6
        ipv6_header = unpack("!IHBB16s16s", packet[14:54])
        next_header = ipv6_header[3]
        if next_header == 6:
            print("TCP packet")
        elif next_header == 17:
            print("UDP packet")
