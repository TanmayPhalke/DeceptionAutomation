import os
import socket
from tkinter import filedialog
import tkinter as tk



def send_chat():
    print("Sending chat audio...")

    # Function to prompt user to select a folder and send its contents
    def send_files():
        root = tk.Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('172.20.10.6', 1234))
                for root, dirs, files in os.walk(folder_selected):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            file_data = f.read()
                            s.sendall(file_data)

   