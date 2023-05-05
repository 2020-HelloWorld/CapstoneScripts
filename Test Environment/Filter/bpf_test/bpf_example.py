import pcapy
from struct import *

# Define the BPF filter expression
filter_expression = "tcp port 80"

# Open the network interface in promiscuous mode
capture = pcapy.open_live("enp0s3", 65536, 1, 0)

# Set the BPF filter
#capture.setfilter(filter_expression)

# Loop through incoming packets and apply the filter
while True:
    (header, packet) = capture.next()
    print(header,"\n",packet)
    # Parse the packet header
    ethernet_header = packet[:14]
    eth_header = unpack('!6s6sH', ethernet_header)
    
    # Parse the IP header
    ip_header = packet[14:34]
    iph = unpack('!BBHHHBBH4s4s', ip_header)
    
    # Parse the TCP header
    tcp_header = packet[34:54]
    tcph = unpack('!HHLLBBHHH', tcp_header)
    
    # Extract the source and destination ports
    source_port = tcph[0]
    dest_port = tcph[1]
    
    # Apply the BPF filter
    if dest_port == 80:
        print("Packet accepted")
    else:
        print("Packet dropped")
