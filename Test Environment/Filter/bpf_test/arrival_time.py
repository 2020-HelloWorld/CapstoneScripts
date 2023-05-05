import pcapy

# Open the network interface in promiscuous mode
capture = pcapy.open_live("enp0s3", 65536, 1, 0)

# Loop through incoming packets and print the timestamp of each packet
while True:
    (header, packet) = capture.next()
    
    # Get the timestamp of the packet
    timestamp = header.getts()
    seconds = timestamp[0]
    microseconds = timestamp[1]
    
    # Print the timestamp in a human-readable format
    print(f"Packet captured at {seconds}.{microseconds:06d}")
