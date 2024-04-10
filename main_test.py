from tkinter import filedialog
import PySimpleGUI as sg
import threading
from generate import generate_chat
from send_chat import send_chat
import trans_hackrf
import hackrf_rx
import socket
import tkinter as tk
import rec_chat as rc
import time
import os

server_mode = 0
client_mode = 0

def start_server_thread():
    server_thread = threading.Thread(target=server_logic)
    server_thread.daemon = True
    server_thread.start()

def start_client_thread():
    client_thread = threading.Thread(target=client_logic)
    client_thread.daemon = True
    client_thread.start()

def start_hackrf_thread(type):
    hackrf_thread = threading.Thread(target=type)
    hackrf_thread.daemon = True
    hackrf_thread.start()


def hackrf_logic_tx():
    os.system('pwd')
    os.system('./DeceptionAutomation/trans_hackrf.py /home/cranky/deceptionautomation/DeceptionAutomation/transfer/1.wav') 
    

def hackrf_logic_rx():
    os.system('hackrf_rx.py') 
    

def server_logic():
    global server_mode, client_mode
    HOST = '172.20.10.6'  # Server's IP address
    PORT = 65432        # Port to listen on

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            conn.sendall(b'Hello from server!')

            while True:
                
                checkmode(server_mode,client_mode)
                start_hackrf_thread(hackrf_logic_tx)
                data = conn.recv(1024)
                if data == b'ack':
                    changemode()
                    checkmode(server_mode,client_mode)

def client_logic():
    global server_mode, client_mode
    HOST = '172.20.10.6'  # Server's IP address
    PORT = 65432        # Port to connect to

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        print('Received', repr(data))

        while True:
            checkmode(server_mode,client_mode)
            start_hackrf_thread(hackrf_logic_rx)
            time.sleep(15)
            changemode()
            s.sendall(b'ack')
            checkmode(server_mode,client_mode)

def checkmode(flag1, flag2):
    if ((flag1 ==1) and (flag2 ==0)):
        print("Tx Mode")
    elif ((flag1 ==0) and (flag2 ==1)):
        print("Rx Mode")


def changemode():
    global server_mode, client_mode

    if server_mode == 1 and client_mode == 0:
        server_mode = 0
        client_mode = 1
    elif server_mode == 0 and client_mode == 1:
        server_mode = 1
        client_mode = 0
    else:
        print('Error: Invalid mode configuration')
    print("Modes changed")

    

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
            # Start local mode actions
            print("Local mode selected")
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
            print("Remote mode selected")

window.close()
