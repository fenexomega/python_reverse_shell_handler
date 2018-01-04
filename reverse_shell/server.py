#!/usr/bin/python3

import socket 
import threading

running = True
HOST = 'localhost'
PORT = 6900
BUFFER = 1024

tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp.bind((HOST,PORT))
tcp.listen(1)
connection,ip = tcp.accept()

class ReadThread(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        global running
        try:
            while running:
                msg = self.conn.recv(1024)
                msg = msg.decode('utf8')
                print(msg,end='')
                if msg == '':
                    print("FECHOU. Pressione Enter para Sair")
                    running = False
                    break
        except:
            self.conn.close()

t1 = ReadThread(connection)
t1.start()

try:
    while running:
        command = input()
        connection.sendall((command + '\n').encode())
finally:
    connection.close()
    tcp.close()
    running = False

