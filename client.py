#client.py
import socket

IP_Port = ('127.0.0.1', 8008)

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mysocket.connect(IP_Port)
print(f'== Connected to {IP_Port[0]} ==')


message = input('Message: ')
mysocket.send(message.encode())

payload = mysocket.recv(1024)
print(f'Server says: {payload.decode()}')