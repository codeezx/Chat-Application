import socket
import threading

# Server Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# List to keep track of connected clients
clients = []

# Function to broadcast messages to all clients
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

# Function to handle individual client
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)  # Receive message from client
            if message:
                print(f"Received: {message.decode('utf-8')}")
                broadcast(message, client_socket)  # Broadcast to others
        except:
            # Remove client from the list and close connection
            clients.remove(client_socket)
            client_socket.close()
            break

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 connections
    print(f"Server started on {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection: {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
