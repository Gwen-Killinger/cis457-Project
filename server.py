#server.py
import socket

IP_Port = ('127.0.0.1', 8008)

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysocket.bind(IP_Port)
mysocket.listen()

while True:
    connection, address = mysocket.accept()
    client_IP = address[0]
    print(f'A TCP connection is opened for {client_IP}')

    received_data = connection.recv(1024)
    print(f'{client_IP} said: {received_data.decode()}')

    connection.send('Goodbye client!'.encode())