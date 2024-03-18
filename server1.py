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
    
    # Prompt client for username
    client_socket.send("Enter your username: ".encode())
    username = client_socket.recv(BUFFER_SIZE).decode()
    
    # Add client to the connected clients list along with username
    connected_clients.append((client_socket, addr, username))

    # Print the list of connected clients
    print("******************")
    print("Connected clients:")
    for _, _, client_username in connected_clients:
        print(f"- Username: {client_username}")

    # Handle data exchange with the client
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print(f"[-] Connection with {addr[0]}:{addr[1]} closed.")
                break
            
            sender_username = get_username_by_socket(client_socket)
            print(f"Received message from {client_username}: {data.decode()}")  # Display received message with username
            
            # Broadcast message to all clients
            broadcast_message = f"{sender_username}: {data.decode()}"
            broadcast_to_clients(broadcast_message, client_socket)
            
        except ConnectionResetError:
            print(f"[-] Connection with {addr[0]}:{addr[1]} forcibly closed.")
            break

    # Remove client from the connected clients list
    connected_clients.remove((client_socket, addr, username))

    # Close the client socket
    client_socket.close()

    # Print updated list of connected clients
    print("******************")
    print("Connected clients:")
    for _, _, client_username in connected_clients:
        print(f"- Username: {client_username}")

# Function to broadcast message to all clients except the sender
def broadcast_to_clients(message, sender_socket):
    for client_socket, _, _ in connected_clients:
        if client_socket != sender_socket:
            client_socket.send(message.encode())

# Function to get username by client socket
def get_username_by_socket(client_socket):
    for _, _, username in connected_clients:
        if _[0] == client_socket:
            return username
    return None

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
