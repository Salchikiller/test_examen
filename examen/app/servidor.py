import socket
import select
from datetime import datetime

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    server_socket.setblocking(False)
    print(f"Server started on port {port}. Waiting for connections...")

    inputs = [server_socket]
    outputs = []
    client_data = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s is server_socket:
                client_socket, client_address = s.accept()
                print(f"Connection from {client_address} has been established.")
                client_socket.setblocking(False)
                inputs.append(client_socket)
                client_data[client_socket] = {'requests': 0}
            else:
                data = s.recv(1024).decode('utf-8').strip()
                if data:
                    client_info = client_data[s]
                    if client_info['requests'] < 3:
                        if data == 'FECHA':
                            response = datetime.now().strftime('%Y-%m-%d')
                        elif data == 'HORA':
                            response = datetime.now().strftime('%H:%M:%S')
                        else:
                            response = 'ERROR'
                        s.send(response.encode('utf-8'))
                        client_info['requests'] += 1
                    if client_info['requests'] == 3:
                        inputs.remove(s)
                        s.close()
                        print(f"Connection closed after 3 requests.")
                else:
                    print("Client disconnected unexpectedly.")
                    inputs.remove(s)
                    s.close()

        for s in exceptional:
            print("Handling exceptional condition for", s.getpeername())
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del client_data[s]

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
