import pcapy
import struct

# Open the network interface in promiscuous mode
capture = pcapy.open_live("enp0s3", 65536, 1, 0)

# Loop through incoming packets and print the departure time of TCP packets
while True:
    (header, packet) = capture.next()
    
    # Extract the TCP header from the packet
    tcp_header = packet[34:54]
    
    # Unpack the header fields using the struct module
    fields = struct.unpack("!HHLLBBHHH", tcp_header)
    
    # Extract the sequence and acknowledgement numbers
    seq_num = fields[2]
    ack_num = fields[3]
    
    # Calculate the departure time (in seconds) as the difference between the acknowledgement and sequence numbers
    departure_time = (ack_num - seq_num) / 1000000.0  # assuming a 1 Mbps link speed
    
    # Print the departure time if the packet is a TCP packet
    if fields[5] & 0x12 == 0x12:  # check for SYN-ACK or ACK flags
        print(f"TCP packet departed {departure_time:.3f} seconds after being sent")
