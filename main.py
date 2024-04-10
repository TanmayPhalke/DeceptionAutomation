import PySimpleGUI as sg
import threading
from generate import generate_chat
from send_chat import send_chat
from trans_rf import transmit_rf
from rx_rf import receive_rf
import socket

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
    HOST = '127.0.0.1'  # Server's IP address
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

# Function to handle client logic
def client_logic():
    # Placeholder for client logic
    HOST = '127.0.0.1'  # Server's IP address
    PORT = 65432        # Port to connect to

    # Initialize client socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Placeholder for client logic
        # For demonstration purposes, receiving a message from the server
        data = s.recv(1024)
        print('Received', repr(data))

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
            start_client_thread()

window.close()
