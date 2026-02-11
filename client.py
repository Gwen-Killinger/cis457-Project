#client.py
import socket

# Host - 127.0.0.1 is localhost 
# Port # - Any port larger than 1023
IP_Port = ('127.0.0.1', 8008)

# Creates socket object with IPv4 and TCP
# AF_INET - IPv4
# SOCK_STREAM - TCP
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects to port opened by the server
mysocket.connect(IP_Port)
print(f'== Connected to {IP_Port[0]} ==')

# Waits for message to be inputted by the user then encodes data and sends to the server
message = input('Message: ')
mysocket.send(message.encode())

# Recieves data sent by server
received_data = mysocket.recv(1024)
print(f'Server says: {received_data.decode()}')