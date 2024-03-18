import socket

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected to server.")

# Receive username prompt from server
username_prompt = client_socket.recv(BUFFER_SIZE).decode()
print(username_prompt, end=' ')
username = input()

# Send username to server
client_socket.send(username.encode())

# Data exchange
while True:
    message = input("Enter message to send (type 'exit' to quit): ")
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode())
    print("[+] Message sent.")

# Close the client socket
client_socket.close()
