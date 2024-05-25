import socket
import sys
from datetime import datetime

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server started on port {port}. Waiting for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")
        
        request_count = 0
        while request_count < 3:
            msg = client_socket.recv(1024).decode('utf-8').strip()
            if not msg:
                break
            if msg == 'FECHA':
                response = datetime.now().strftime('%Y-%m-%d')
            elif msg == 'HORA':
                response = datetime.now().strftime('%H:%M:%S')
            else:
                response = 'ERROR'
            client_socket.send(response.encode('utf-8'))
            request_count += 1
        
        client_socket.close()
        print(f"Connection from {client_address} closed after {request_count} requests.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_server(port)
