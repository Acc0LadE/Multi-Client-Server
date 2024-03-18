import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# List to store connected clients
connected_clients = []

# Function to handle client connections
def handle_client(client_socket, addr):
    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
    
    # Add client to the connected clients list
    connected_clients.append((client_socket, addr))

    # Print the list of connected clients
    print("******************")
    print("Connected clients:")
    for client, client_addr in connected_clients:
        print(f"- Hostname: {client_addr[0]}, IP: {client_addr[1]}")

    # Handle data exchange with the client
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print(f"[-] Connection with {addr[0]}:{addr[1]} closed.")
                break
            print(f"Received data from {addr[0]}:{addr[1]}: {data.decode()}")
        except ConnectionResetError:
            print(f"[-] Connection with {addr[0]}:{addr[1]} forcibly closed.")
            break

    # Remove client from the connected clients list
    connected_clients.remove((client_socket, addr))

    # Close the client socket
    client_socket.close()

    # Print updated list of connected clients
    print("******************")
    print("Connected clients:")
    for client, client_addr in connected_clients:
        print(f"- Hostname: {client_addr[0]}, IP: {client_addr[1]}")

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

# Main server loop
while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
