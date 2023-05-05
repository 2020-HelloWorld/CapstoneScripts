import pcapy
import struct
import socket

DEVICE = "enp0s3"

capture = pcapy.open_live(DEVICE, 65536, 1, 0)

while True:
    (header, packet) = capture.next()
    
    ethernet_header = packet[:14]
    eth_header = struct.unpack('!6s6sH', ethernet_header)
    eth_protocol = socket.ntohs(eth_header[2])
    
    eth_length = 14
    
    if eth_protocol == 8:  # IPv4
        
        # Protocol
        ip_header = struct.unpack("!BBHHHBBH4s4s", packet[14:34])
        protocol = ip_header[6]
        if protocol == 6:
            print("TCP packet")
            
            # Departure time
            # Extract the TCP header from the packet
            tcp_header = packet[34:54]
            
            # Check if the TCP header contains the timestamp option
            if (tcp_header[12] & 0xf0) >> 4 > 5:
                # Extract the timestamp option from the TCP header
                timestamp_option = tcp_header[20:24]
                if len(timestamp_option) >= 8:
                    fields = struct.unpack("!LL", timestamp_option[:8])
                    timestamp = fields[0]
                    timestamp_echo = fields[1]
                    print("TCP timestamp: %d, TCP timestamp echo reply: %d" % (timestamp, timestamp_echo))
                else:
                    print("Not enough data to unpack TCP timestamp option")
                                
        elif protocol == 17:
            print("UDP packet")
            
        # IP address
        ip_header = packet[eth_length:20+eth_length]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        src_ip = socket.inet_ntoa(iph[8])
        dst_ip = socket.inet_ntoa(iph[9])
        
        # Print the source and destination IP addresses
        print("Source IP: ", src_ip)
        print("Destination IP: ", dst_ip)
        
        
        # Arrival time
        timestamp = header.getts()
        seconds = timestamp[0]
        microseconds = timestamp[1]
        
        # Print the timestamp in a human-readable format
        print(f"Packet captured at {seconds}.{microseconds:06d}")
        
        
        

    elif eth_protocol == 1544:  # IPv6
        ipv6_header = struct.unpack("!IHBB16s16s", packet[14:54])
        next_header = ipv6_header[3]
        if next_header == 6:
            print("TCP packet - IPV6")
        elif next_header == 17:
            print("UDP packet - IPV6")
    print("----------------------------------------------------------------")
            
    
    

