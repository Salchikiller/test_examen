import socket

def start_client(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', port))
        print(f"Connected to server at 127.0.0.1:{port}")
        
        for _ in range(3):
            try:
                msg = input("Enter message for server (FECHA or HORA): ")
                if msg not in ['FECHA', 'HORA']:
                    msg = 'ERROR'
                client_socket.send(msg.encode('utf-8'))
                
                response = client_socket.recv(1024).decode('utf-8')
                if not response:
                    print("Server has disconnected unexpectedly.")
                    break
                
                print(f"Response from server: {response}")
            except ConnectionResetError:
                print("Server has disconnected unexpectedly.")
                break
        
        client_socket.close()
        print("Connection closed after 3 requests or server disconnection.")
    
    except ConnectionRefusedError:
        print("Server is not available or refused the connection.")
    except ConnectionResetError:
        print("Server has disconnected unexpectedly.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    port = int(input("Enter server port: "))
    start_client(port)
