import pcapy
from struct import *

# Define the BPF filter expression
filter_expression = "tcp port 80"

# Open the network interface in promiscuous mode
capture = pcapy.open_live("enp0s3", 65536, 1, 0)

# Set the BPF filter
capture.setfilter(filter_expression)

# Create a new pcap file for output
output_file = pcapy.open_dead(pcapy.DLT_EN10MB, 65536)
dumper = output_file.dump_open("output.pcap")

# Loop through incoming packets and apply the filter
while True:
    (header, packet) = capture.next()
    
    # Save the packet to the pcap file
    dumper.dump(header, packet)
