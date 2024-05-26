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
    
    def send_response(self, client_socket, message):
        response = self.generate_response(message)
        client_socket.send(response.encode('utf-8'))

    def handle_client_connection(self, client_socket, client_data):
        data = client_socket.recv(1024).decode('utf-8').strip()
        if data:
            client_info = client_data[client_socket]
            if client_info['requests'] < 3:
                self.send_response(client_socket, data)
                client_info['requests'] += 1
            if client_info['requests'] == 3:
                return True  # Indica que la conexión debe cerrarse
        else:
            print("Client disconnected unexpectedly.")
            return True  # Indica que la conexión debe cerrarse
        return False

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
                    if self.handle_client_connection(s, client_data):
                        inputs.remove(s)
                        s.close()
                        del client_data[s]
                        print(f"Connection closed.")

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
