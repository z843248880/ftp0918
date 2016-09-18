#!/usr/bin/env python
#coding:utf-8


import socket,os,time

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',9545))
server.listen()

while True:
    conn,addr = server.accept()
    while True:
        data = conn.recv(10240)
        if not data:break  
        result = os.popen(data.decode()).read()
        if result == '':
            result = 'command not found.'

        conn.send(str(len(result.encode('UTF-8'))).encode('UTF-8'))
        conn.recv(1024)
#         time.sleep(0.5)
        conn.send(result.encode('UTF-8'))
server.close()