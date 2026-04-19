# server.py
import socket
import threading

clients = []
usernames = {'': 0}

def send_private(message, recipient_username):

    for conn, uname in usernames.items():
        if uname == recipient_username:

            try:
                conn.send(message)

            except:
                conn.close()
                if conn in clients:
                    clients.remove(conn)


def clientHandler(connection, address):

    username = usernames[connection]

    while True:

        try:
            data = connection.recv(1024)
        except:
            break


        if not data:
            break


        # try decoding text
        try:
            message = data.decode()
        except:
            message = None


        # quit
        if message == "quit":
            break


        # file transfer
        elif message is not None and message.startswith("/file"):

            try:

                filename = message.split(" ",1)[1]

                print(f"{username} sent file: {filename}")

                broadcast(
                    f"{username} sent file: {filename}".encode(),
                    None
                )

                file_bytes = connection.recv(1024)

                broadcast(file_bytes, None)

            except:
                print("file transfer failed")


        # private message
        elif message is not None and message.startswith("@"):

            parts = message.split(" ",1)

            if len(parts) < 2:

                connection.send(
                    "Invalid DM format. Use: @username message".encode()
                )

                continue


            target = parts[0][1:]

            private_msg = parts[1]


            if target not in usernames.values():

                connection.send(
                    f"user '{target}' not found".encode()
                )

                continue

            send_private(
                f"(DM) {username}: {private_msg}".encode(),
                target
            )


        # normal chat
        elif message is not None:

            full_message = f"{username}: {message}"
            print(full_message)
            broadcast(full_message.encode(), None)

    print(f"{username} disconnected")

    if connection in clients:
        clients.remove(connection)

    if connection in usernames:
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

