#!/usr/bin/env python
#coding:utf-8

import socket,os,time,hashlib

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',9552))
server.listen()

while True:
    conn,addr = server.accept()
    while True:
        data = conn.recv(10240)
        if not data:break  
        cmd,filename = data.decode().split()
        if os.path.isfile(filename):
            m = hashlib.md5()
            filesize = os.stat(filename).st_size
            conn.send(str(filesize).encode())
            conn.recv(1024)
            with open(filename) as f:
                for line in f:
                    m.update(line.encode())
                    conn.send(line.encode())
#         time.sleep(0.5)
        conn.send(m.hexdigest().encode())
        print('send done.')
server.close()