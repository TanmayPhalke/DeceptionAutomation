import os
import socket
from tkinter import filedialog
import tkinter as tk



# Function to receive files and save them along with folder name
def rx_files():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('192.20.10.6', 1234))
        s.listen()
        conn, addr = s.accept()
        with conn:
            folder_name = conn.recv(1024).decode()
            os.makedirs(folder_name, exist_ok=True)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file_name = os.path.basename(data)
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'wb') as f:
                    f.write(data)

