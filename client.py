#client.py
import socket
import threading
from tkinter.font import names
import os


def senderThread(mysocket):
    while True:
        # Waits for message to be inputted by the user then encodes data and sends to the server
        message = input('Message: ')

        if message.startswith("/file"):
            try:
                _, filename = message.split(" ", 1)
                sendFile(mysocket, filename)
            except:
                print("Usage: /file filename")
            continue

        try:
            mysocket.send((message).encode())
        except:
            print("Not connected to server client closing...")
            break
        if message == "quit":
            mysocket.send("quit".encode())
            mysocket.close()
            break
    return

def listenerThread(mysocket):

    while True:

        try:

            received_data = mysocket.recv(1024)

        except:

            print("Client Closing...")

            break


        # try decoding message normally
        try:

            decoded = received_data.decode()


            # server notifying file incoming
            if "sent file:" in decoded:

                print("\n" + decoded)

                filename = decoded.split("sent file: ")[1]

                # receive file bytes
                file_bytes = mysocket.recv(1024)

                with open("received_" + filename, "wb") as f:

                    f.write(file_bytes)

                print(f"File saved as received_{filename}")


            else:

                print("\r" + " " * 50 + "\r", end="")

                print(decoded)

                print('Message: ', end="", flush=True)


        # binary data fallback
        except:

            with open("received_file", "ab") as f:

                f.write(received_data)

            print("\nReceiving file data...")


        if received_data.decode(errors="ignore") == "Server Closing":

            mysocket.close()

            break

def nameSanitizer(name):
    while True:
        name = input("Enter a Username Using only Alphanumeric Characters: ")
        if name.isalnum():
            mysocket.send(name.encode())
            break
    return 0

# Host - 127.0.0.1 is localhost
# Port # - Any port larger than 1023
IP_Port = ('127.0.0.1', 6767)

# Creates socket object with IPv4 and TCP
# AF_INET - IPv4
# SOCK_STREAM - TCP
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects to port opened by the server
mysocket.connect(IP_Port)

# Username setup
while True:
    msg = mysocket.recv(1024).decode()

    if msg == "Please Enter a Username":
        name = ''
        nameSanitizer(name)
    elif msg == "Username is Already Taken":
        print("Username already taken, try again.")
        nameSanitizer(name)
    else:
        break

print(f'== Connected to {IP_Port[0]} ==')
print('--Type quit to exit')

threadSend = threading.Thread(target=senderThread, args=(mysocket,))
threadListen = threading.Thread(target=listenerThread, args=(mysocket,))

threadSend.start()
threadListen.start()


def sendFile(mysocket, filename):
    if not os.path.exists(filename):
        print("File not found")
        return

    with open(filename, "rb") as f:
        data = f.read()

    mysocket.send(f"/file {filename}".encode())
    mysocket.send(data)
