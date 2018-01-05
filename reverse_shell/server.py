#!/usr/bin/python3

import socket 
import threading
import time
import sys
import select

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
                msg = self.conn.recv(BUFFER)
                msg = msg.decode('utf8')
                print(msg,end='')
                if msg == '':
                    print("FECHOU.")
                    running = False
                    break
        except:
            pass
        finally:
            self.conn.close()

class WriteThread(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        global running
        try:
            while running:
                time.sleep(0.05)
                if select.select([sys.stdin,],[],[],0.0)[0]:
                    c = input() + '\n'
                    self.conn.send(c.encode())
                    sys.stdin.flush()
                
        except:
            print("Connection Exited")
        finally:
            running = False
            self.conn.close()


print("connection received from {}".format(ip))
t1 = ReadThread(connection)
t1.start()
t2 = WriteThread(connection)
t2.start()

try:
    t1.join()
    t2.join()
finally:
    connection.close()
    tcp.close()
    running = False

