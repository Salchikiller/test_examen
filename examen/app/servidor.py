# app/servidor.py

import socket
import select
from datetime import datetime

class Server:
    def __init__(self, port):
        self.port = port

    def generate_response(self, message):
        if message == 'FECHA':
            return datetime.now().strftime('%Y-%m-%d')
        elif message == 'HORA':
            return datetime.now().strftime('%H:%M:%S')
        else:
            return 'ERROR'

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', self.port))
        server_socket.listen(5)
        server_socket.setblocking(False)
        print(f"Server started on port {self.port}. Waiting for connections...")

        inputs = [server_socket]
        client_data = {}

        while inputs:
            readable, writable, exceptional = select.select(inputs, [], inputs)

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
                            response = self.generate_response(data)
                            s.send(response.encode('utf-8'))
                            client_info['requests'] += 1
                        if client_info['requests'] == 3:
                            inputs.remove(s)
                            s.close()
                            del client_data[s]
                            print(f"Connection closed after 3 requests.")
                    else:
                        print("Client disconnected unexpectedly.")
                        inputs.remove(s)
                        s.close()
                        del client_data[s]

            for s in exceptional:
                print(f"Handling exceptional condition for {s.getpeername()}")
                inputs.remove(s)
                s.close()
                if s in client_data:
                    del client_data[s]

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python servidor.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = Server(port)
    server.start_server()
