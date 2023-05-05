import pcapy
import struct
import socket
import csv
import os
# import matplotlib.pyplot as plt
# import threading
# import pandas as pd

# Constant Values
UDP  = 0
TCP  = 1
IPV6 = 0
IPV4 = 1
DEVICE = "enp0s3"
FILE = "data.csv"

def init(device):
    capture = pcapy.open_live(device, 65536, 1, 0)
    return capture

def get_eth_header(packet):
    ethernet_header = packet[:14]
    eth_header = struct.unpack('!6s6sH', ethernet_header)
    eth_protocol = socket.ntohs(eth_header[2])
    eth_length = 14
    return eth_protocol,eth_length
    
def get_protocol(eth_protocol:int,packet):
    if eth_protocol == 8:  # IPv4
        ip_header = struct.unpack("!BBHHHBBH4s4s", packet[14:34])
        protocol = ip_header[6]
        if protocol == 6: #TCP
            return TCP,IPV4
        elif protocol == 17: #UDP
            return UDP,IPV4
    else:
        return None,None
        
def get_departure_time(packet):
    # Extract the TCP header from the packet
    tcp_header = packet[34:54]
    
    # Check if the TCP header contains the timestamp option
    if (tcp_header[12] & 0xf0) >> 4 > 5:
        # Extract the timestamp option from the TCP header
        timestamp_option = tcp_header[20:24]
        timestamp = None
        if (tcp_header[12] & 0xf0) >> 4 > 5:
                # Extract the timestamp option from the TCP header
                timestamp_option = tcp_header[20:24]
                if len(timestamp_option) >= 8:
                    fields = struct.unpack("!LL", timestamp_option[:8])
                    timestamp = fields[0]
                    timestamp_echo = fields[1]                      
        return timestamp
    
def get_arrival_time(header):
    timestamp = header.getts()
    seconds = timestamp[0]
    microseconds = timestamp[1]
    arrival_time = float(f"{seconds}.{microseconds}")
    return arrival_time
    
def get_ip_addr(packet,eth_length:int):
    ip_header = packet[eth_length:20+eth_length]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    iph_length = ihl * 4
    src_ip = socket.inet_ntoa(iph[8])
    dst_ip = socket.inet_ntoa(iph[9])
    return src_ip,dst_ip

def csv_init(filename:str):
    fields = ['version','protocol','src_ip', 'des_ip', 'arrival_time', 'departure_time']
    files = os.listdir("./")
    csvfile = open(filename, 'a')
    csvwriter = csv.writer(csvfile)
    if filename not in files:
        # writing the fields
        csvwriter.writerow(fields)
    return csvwriter
         
def write_csv(csvwriter,protocol:int,version:int,src_ip,des_ip,arrival_time,departure_time):
    data = [protocol,version,src_ip,des_ip,arrival_time,departure_time]
    csvwriter.writerow(data)

# def plot_live_packet_presence(filename=FILE):
#     while True:
#         try:
#             data = pd.read_csv(filename)
#             # filter the data to include only the desired sender and receiver
#             src_ip = "34.160.144.191"
#             des_ip = "10.0.2.4"
#             data = data[(data['src_ip'] == src_ip) & (data['des_ip'] == des_ip)]

#             # calculate the packet presence by cumulatively summing the packets that are present
#             data['presence'] = (data['departure_time'].notna() | data['protocol']==UDP).cumsum()

#             # create a scatter plot of packet presence vs arrival time
#             fig, ax = plt.subplots()
#             ax.scatter(data['arrival_time'], data['presence'])
#             ax.set_xlabel("Arrival Time (s)")
#             ax.set_ylabel("Packet Presence")
            
#             print(data.head())
            
#             # show the plot
#             plt.show()
#         except:
#             pass

   
def start_capture():
    capture = init(DEVICE)
    csvwriter = csv_init(filename=FILE)
    while True:
        (header, packet) = capture.next()
        eth_protocol,eth_length = get_eth_header(packet=packet)
                
        protocol = None 
        version = None
        departure_time = None
        arrival_time = None
        src_ip = None 
        des_ip = None
        
        protocol,version = get_protocol(eth_protocol=eth_protocol,packet=packet)
    
        if version==IPV4:
            src_ip,des_ip = get_ip_addr(packet=packet,eth_length=eth_length)
            arrival_time = get_arrival_time(header=header)
            if protocol==TCP:
                try:
                    departure_time = get_departure_time(packet=packet)
                except:
                    pass
        write_csv(csvwriter = csvwriter,protocol=protocol,version=version,src_ip=src_ip,des_ip=des_ip,arrival_time=arrival_time,departure_time=departure_time)


# def main():
#     # create two threads, one for capturing packets and the other for plotting the graph
#     t1 = threading.Thread(target=start_capture)
#     # t2 = threading.Thread(target=plot_live_packet_presence)

#     # start both threads
#     t1.start()
#     # t2.start()

#     # wait for both threads to finish
#     t1.join()
#     # t2.join()

if __name__ == '__main__':
    # main()
    start_capture()
