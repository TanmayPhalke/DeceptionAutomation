from tkinter import filedialog
import PySimpleGUI as sg
import threading
from generate import generate_chat
from send_chat import send_chat
from trans_rf import transmit_rf
from rx_rf import receive_rf
import socket
import tkinter as tk
import rec_chat as rc
import time

server_mode = 0
client_mode = 0


# Function to start the server in a daemon thread
def start_server_thread():
    server_thread = threading.Thread(target=server_logic)
    server_thread.daemon = True
    server_thread.start()

# Function to start the client in a daemon thread
def start_client_thread():
    client_thread = threading.Thread(target=client_logic)
    client_thread.daemon = True
    client_thread.start()


# Function to handle server logic
def server_logic():
    # Placeholder for server logic
    HOST = '172.20.10.6'  # Server's IP address
    PORT = 65432        # Port to listen on

    # Initialize server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)

            # Placeholder for server logic
            # For demonstration purposes, sending a message to the client
            conn.sendall(b'Hello from server!')
            checkmode(server_mode, client_mode)
            time.sleep(10)
            #conn.sendall(b'ack')
            changemode(s)
            data = conn.recv(1024)
            print("recd", repr(data))
            if data.decode("utf-8") == 'ack':
                changemode(conn)
        

            
        
        checkmode(server_mode, client_mode)

        
            


def checkmode(flag1, flag2):
    if ((flag1 ==1) and (flag2 ==0)):
        print("Tx Mode")
    elif ((flag1 ==0) and (flag2 ==1)):
        print("Rx Mode")

# Function to handle client logic
def client_logic():
    # Placeholder for client logic
    HOST = '172.20.10.6'  # Server's IP address
    PORT = 65432        # Port to connect to

    # Initialize client socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        

        # Placeholder for client logic
        # For demonstration purposes, receiving a message from the server
        data = s.recv(1024)
        print('Received', repr(data))
        checkmode(server_mode,client_mode)
        
        data = s.recv(1024)
        print("recd", repr(data))
        if data.decode("utf-8") == 'ack':
            changemode(s)
        
        checkmode(server_mode,client_mode)

        time.sleep(15)
        changemode(s)

    
        

def changemode(conn):
    conn.sendall(b'ack')
    global server_mode, client_mode

    if server_mode == 1 and client_mode == 0:
        server_mode = 0
        client_mode = 1
    elif server_mode == 0 and client_mode == 1:
        server_mode = 1
        client_mode = 0
    else:
        print('Error: Invalid mode configuration')
    print("modes changed")


def rec_logic():
    client_thread = threading.Thread(target=rc.rx_files)
    client_thread.daemon = True
    client_thread.start()


# GUI layout
layout = [
    [sg.Text("Select Mode:")],
    [sg.Radio("Local Mode", "MODE", default=True, key='local'), sg.Radio("Remote Mode", "MODE", key='remote')],
    [sg.Button('Submit')],
]

# Create the GUI window
window = sg.Window('Chat Program', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Submit':
        if values['local']:
            server_mode = 1
            local_layout = [
                [sg.Text("Local Mode Options:")],
                [sg.Button('Generate Chat'), sg.Button('Send Chat Audio'), sg.Button('Start Deception Program'), sg.Button('Exit')],
            ]
            local_window = sg.Window('Local Mode', local_layout)
            while True:
                local_event, local_values = local_window.read()
                if local_event == sg.WINDOW_CLOSED or local_event == 'Exit':
                    local_window.close()
                    break
                elif local_event == 'Generate Chat':
                    generate_chat()
                elif local_event == 'Send Chat Audio':
                    send_chat()
                elif local_event == 'Start Deception Program':
                    start_server_thread()

        elif values['remote']:
            client_mode = 1
            start_client_thread()
            rec_logic()

window.close()
