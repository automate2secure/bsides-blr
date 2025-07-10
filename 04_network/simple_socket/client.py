#!/usr/bin/python3

import socket

# Configuration
HOST = '13.232.135.193'  # Change to the server IP if testing remotely
PORT = 13375
START_TOKEN = "#bsides# "
END_TOKEN = " #end#"


def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        welcome_msg = client_socket.recv(1024).decode()
        print(welcome_msg)
        message = f"{START_TOKEN}{command}{END_TOKEN}"
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"[SERVER RESPONSE] {response}")


if __name__ == "__main__":
    print("Seasides Text Transfer Protocol (SSTP) Client")
    while True:
        cmd = input("Enter command (or 'exit' to quit): ")
        if cmd.lower() == "exit":
            break
        send_command(cmd)
