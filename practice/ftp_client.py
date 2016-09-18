#!/usr/bin/env python
#coding:utf-8

import socket,hashlib

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',9552))

while True:
    u_input = input('>')
    if len(u_input) == 0:continue
    cmd,filename = u_input.split()
    if cmd.startswith('get'):
        client.send(u_input.encode())
        data_size = client.recv(1024).decode()
        client.send('OK'.encode())
        m = hashlib.md5()
        receive_size = 0
        with open(filename + '.new' ,'w') as f:
            while receive_size < int(data_size):
                if int(data_size) - receive_size > 1024:
                    size = 1024
                else:
                    size = int(data_size) - receive_size
                data = client.recv(size)
                receive_size += len(data)
                m.update(data)
                f.write(data.decode())
            else:
                new_md5 = m.hexdigest()
                print('total length is :',receive_size)
        server_md5 = client.recv(1024).decode()
        print('server_mad5:',server_md5)
        print('new_md5',new_md5)
client.close()