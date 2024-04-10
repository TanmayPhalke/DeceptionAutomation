import PySimpleGUI as sg
from generate import generate_chat
from send_chat import send_chat
from trans_rf import transmit_rf
from rx_rf import receive_rf
import threading

# Function to start the server in a daemon thread
def start_server_thread():
    # Placeholder function for server logic
    print("Starting server...")

# Function to start the client in a daemon thread
def start_client_thread():
    # Placeholder function for client logic
    print("Starting client...")

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
                    start_server_thread()  # Placeholder for server logic
        elif values['remote']:
            start_client_thread()  # Placeholder for client logic

window.close()
