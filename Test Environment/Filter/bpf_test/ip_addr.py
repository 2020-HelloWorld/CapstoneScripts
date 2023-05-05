"""
In this example, we first parse the Ethernet header, which is the first 14 bytes of the packet. We extract the protocol number from the header, which tells us whether the packet is an IPv4 or IPv6 packet.

If the protocol is IPv4 (protocol number 0x0800), we extract the IPv4 header from the packet, which is the next 20 bytes after the Ethernet header. We then unpack the header using the unpack() function and the corresponding format string. The source and destination IP addresses are located in bytes 12-15 and 16-19 of the IP header, respectively.

We use the socket.inet_ntoa() function to convert the IP addresses from binary form to the more familiar dotted decimal notation. Finally, we print the source and destination IP addresses to the console.

"""

import pcapy
import socket
from struct import *

# Open the network interface in promiscuous mode
capture = pcapy.open_live("enp0s3", 65536, 1, 0)

# Loop through incoming packets and extract IP addresses
while True:
    (header, packet) = capture.next()

    # Parse the Ethernet header (14 bytes)
    eth_length = 14
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])

    # Parse the IP header (20 bytes)
    if eth_protocol == 8: # Ethernet type 0x0800 (IPv4)
        ip_header = packet[eth_length:20+eth_length]
        iph = unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        src_ip = socket.inet_ntoa(iph[8])
        dst_ip = socket.inet_ntoa(iph[9])
        
        # Print the source and destination IP addresses
        print("Source IP: ", src_ip)
        print("Destination IP: ", dst_ip)
    else:
        print("IPV6 Packet")
    break