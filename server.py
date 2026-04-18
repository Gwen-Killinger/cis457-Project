# server.py
import socket
import threading

clients = []
usernames = {'': 0}

def clientHandler(connection, address):
    username = usernames[connection]

    while True:
        try:
            data = connection.recv(1024)
        except:
            break
        if not data:
            break

        message = data.decode()
        if message == "quit":
            break

        full_message = f"{username}: {message}"
        print(full_message)
        broadcast(full_message.encode(), None)

    # Cleanup on disconnect
    print(f"{username} disconnected")

    clients.remove(connection)
    del usernames[connection]
    connection.close()

    broadcast(f"{username} left the chat".encode(), None)

def broadcast(message, sender):
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()
            if client in clients:
                clients.remove(client)

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

# Program waits here until a client connect, accept() returns a socket object for
# the connection and a tuple (host, port) for the connected client.
print("Server is running...")

while True:
    connection, address = mysocket.accept()

    # Asks for a username
    connection.send("Please Enter a Username".encode())
    username = connection.recv(1024).decode()

    # Ensures unique username
    while username in usernames.values():
        connection.send("Username is Already Taken".encode())
        username = connection.recv(1024).decode()

    # Save user
    clients.append(connection)
    usernames[connection] = username

    print(f"{username} connected from {address}")

    # Notify everyone
    broadcast(f"{username} has joined the chat".encode(), None)

    thread = threading.Thread(target=clientHandler, args=(connection, address))
    thread.start()