import socket
import struct

def tcp_server():
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = 'localhost'
    port = 8000
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on {host}:{port}")

    while True:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"Received connection from {client_address}")

        # Receive packet from client
        packet = client_socket.recv(1024)

        # Extract timestamp from packet header
        timestamp_bytes = packet[24:28]
        timestamp = struct.unpack("!L", timestamp_bytes)[0]
        print(f"Received packet with timestamp: {timestamp}")

        # Close the client socket
        client_socket.close()

    # Close the server socket
    server_socket.close()

if __name__ == '__main__':
    tcp_server()
