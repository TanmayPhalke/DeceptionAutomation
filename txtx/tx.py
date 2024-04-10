import os
import socket
import time
from tkinter import Tk, filedialog

SERVER_HOST = '127.0.0.1'  # Change to your server IP
SERVER_PORT = 12345  # Change to your server port

def transfer_files():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)  # Listen for up to 5 connections
    print("Server listening on port", SERVER_PORT)
    
    while True:
        conn, addr = server_socket.accept()
        print("Connection established with", addr)
        
        root = Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select folder to transfer")
        root.destroy()
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".wav"):
                file_path = os.path.join(folder_path, filename)
                file_size = os.path.getsize(file_path)
                conn.sendall(str(file_size).encode())  # Send file size first
                with open(file_path, 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        conn.sendall(data)
        
        print("Files sent successfully")
        conn.close()

def receive_files():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server")
    
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder to receive files")
    root.destroy()
    
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

# Example usage:
# Run transfer_files on the sender side and receive_files on the receiver side.

transfer_files()