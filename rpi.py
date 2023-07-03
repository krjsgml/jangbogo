import socket
from _thread import *
import time

HOST = '172.30.1.63'
PORT = 3333

print('connect server')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


while True:
    data = client_socket.recv(1024)
    sig = data.decode()

    if sig == '1':
        print('linear down ------ ')
        time.sleep(7)
        tracking_motor = 1

    elif sig == '0':
        tracking_motor = 0
        print('linear up ------ ')
        time.sleep(7)

    if tracking_motor == 1:
        if sig == 'w':
            print("left top")

        elif sig == 'e':
            print("center top")
        
        elif sig == 'r':
            print("right top")
        
        elif sig == 's':
            print("left middle")

        elif sig == 'd':
            print("center middle")

        elif sig == 'f':
            print("right middle")

        elif sig == 'x':
            print("left bottom")

        elif sig == 'c':
            print("center bottom")

        elif sig == 'v':
            print("right bottom")

        elif sig == 'q':
            print('stop')
    
    elif tracking_motor == 0:
        continue

    