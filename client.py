#client.py
import socket
import threading

def senderThread(mysocket):
    while True:
        # Waits for message to be inputted by the user then encodes data and sends to the server
        message = input('Message: ')
        try:
            mysocket.send((message).encode())
        except:
            print("Not connected to server client closing...")
            break
        if message == "quit":
            mysocket.close()
            break
    return

def listenerThread(mysocket):
    while True:
        # Recieves data sent by server
        try:
            received_data = mysocket.recv(1024)
        except:
            print("Client Closing...")
            break
        print("\r" + " " * 50 + "\r", end="", flush=True)
        print(f'Server: {received_data.decode()}')
        print('Message: ', end="", flush=True)

        if received_data.decode() == 'Server Closing':
            mysocket.close()
            break
    return


# Host - 127.0.0.1 is localhost 
# Port # - Any port larger than 1023
IP_Port = ('127.0.0.1', 6767)

# Creates socket object with IPv4 and TCP
# AF_INET - IPv4
# SOCK_STREAM - TCP
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects to port opened by the server
mysocket.connect(IP_Port)
print(f'== Connected to {IP_Port[0]} ==')
print('--Type quit to exit')

threadSend = threading.Thread(target=senderThread, args=(mysocket,))
threadListen = threading.Thread(target=listenerThread, args=(mysocket,))

threadSend.start()
threadListen.start()
