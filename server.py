#server.py
import socket

# Host - 127.0.0.1 is localhost 
# Port # - Any port larger than 1023
IP_Port = ('127.0.0.1', 8008)
 
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
connection, address = mysocket.accept()

client_IP = address[0]
print(f'A TCP connection is opened for {client_IP}')

# Recieves endoced message sent by the user
received_data = connection.recv(1024)
print(f'{client_IP} said: {received_data.decode()}')

# Reply message sent to the client
connection.send('Goodbye client!'.encode())

# Closes Socket
mysocket.close()