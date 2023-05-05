import pcapy
import struct

# Open the network interface in promiscuous mode
capture = pcapy.open_live("enp0s3", 65536, 1, 0)

# Loop through incoming packets and print the departure time of TCP packets with timestamp options
while True:
    (header, packet) = capture.next()
    
    # Extract the TCP header from the packet
    tcp_header = packet[34:54]
    
    # Check if the TCP header contains the timestamp option
    if (tcp_header[12] & 0xf0) >> 4 > 5:
        # Extract the timestamp option from the TCP header
        timestamp_option = tcp_header[20:24]
        
        # Unpack the timestamp fields using the struct module
        fields = struct.unpack("!LL", timestamp_option)
        
        # Extract the sender's timestamp value
        timestamp_value = fields[0]
        
        # Print the sender's timestamp value
        print(f"TCP packet departed at time {timestamp_value}")
