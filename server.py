#server.py
import socket
import threading

clients = []

def clientHandler(connection, address):
    while True:
        data = connection.recv(1024)
        if not data:
            print("\nClosing Connection")
            break
        print("\r" + " " * 50 + "\r", end="")
        print(f"Client: {data.decode()}")
        print("Message: ", end="", flush=True)
    connection.close()

def serverSender():
    while True:
        message = input("Message: ")
        if message == "quit":
            break
        if clients:
            clients[0].send((message).encode())
    connection.close()
    mysocket.close()


# Host - 127.0.0.1 is localhost 
# Port # - Any port larger than 1023
IP_Port = ('127.0.0.1', 6767)
 
# Creates socket object with IPv4 and TCP
# AF_INET - IPv4
# SOCK_STREAM - TCP
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binds (Host, Port) to created socket
mysocket.bind(IP_Port)

# Begins listening on the specifed socket
mysocket.listen()
serverSendingThread = threading.Thread(target=serverSender)
serverSendingThread.start()

# Program waits here until a client connect, accept() returns a socket object for 
# the connection and a tuple (host, port) for the connected client.
connection, address = mysocket.accept()
clients.append(connection)
clientListenerThread = threading.Thread(target=clientHandler, args=(connection, address))
clientListenerThread.start()