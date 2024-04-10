import socket
import time
import os

SERVER_HOST = '172.20.10.6'  # Change to your server IP
SERVER_PORT = 12345  # Change to your server port

def rx_files():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server")
    
    folder_path = ".\\received_files"
    
    while True:
        file_size_data = client_socket.recv(1024)
        if not file_size_data:
            break
        file_size = int(file_size_data.decode())
        received = 0
        with open(os.path.join(folder_path, f"received_{time.time()}.wav"), 'wb') as file:
            while received < file_size:
                data = client_socket.recv(1024)
                file.write(data)
                received += len(data)
    
    print("Files received successfully")