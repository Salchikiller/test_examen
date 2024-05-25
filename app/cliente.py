import socket

def start_client(server_address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, port))
    print(f"Connected to server at {server_address}:{port}")
    
    for _ in range(3):
        msg = input("Enter message for server (FECHA or HORA): ")
        if msg not in ['FECHA', 'HORA']:
            msg = 'ERROR'
        client_socket.send(msg.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Response from server: {response}")
    
    client_socket.close()
    print("Connection closed after 3 requests.")

if __name__ == "__main__":
    server_address = input("Enter server address: ")
    port = int(input("Enter server port: "))
    start_client(server_address, port)
