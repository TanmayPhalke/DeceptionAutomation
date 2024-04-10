import os
import socket
import zipfile
from tkinter import Tk, filedialog

# Sender's IP address and port
SENDER_HOST = '172.20.10.4'  # Change to sender's IP address
SENDER_PORT = 65431  # Change to sender's port
BUFFER_SIZE = 1024  # Buffer size for sending data

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

def send_zip(zip_path):
    print("Sending zip file...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SENDER_HOST, SENDER_PORT))
        
        with open(zip_path, 'rb') as file:
            data = file.read(BUFFER_SIZE)
            while data:
                s.send(data)
                data = file.read(BUFFER_SIZE)
        print("Zip file sent successfully.")

def select_and_send_folder():
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder to send")
    root.destroy()
    
    zip_path = folder_path + '.zip'
    zip_folder(folder_path, zip_path)
    print("Folder zipped successfully.")
    
    send_zip(zip_path)

# Example usage:
select_and_send_folder()
