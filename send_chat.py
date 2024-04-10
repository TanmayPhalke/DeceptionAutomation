import os
import socket
import tkinter as tk
from tkinter import filedialog

def send_chat():
    print("Sending chat audio...")
    transfer_files()

SERVER_HOST = '172.20.10.6'  # Change to your server IP
SERVER_PORT = 12345  # Change to your server port



def transfer_files():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)  # Listen for up to 5 connections
    print("Server listening on port", SERVER_PORT)
    file_counter = 0
    
    while True:
        conn, addr = server_socket.accept()
        print("Connection established with", addr)
        
        root = tk.Tk()
        #oot.withdraw()
        folder_path = filedialog.askdirectory(title="Select folder to transfer")
        root.destroy()
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".wav"):
                file_counter+=1
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
        print(file_counter)
        conn.close()