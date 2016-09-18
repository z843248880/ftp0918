#!/usr/bin/env python
#coding:utf-8


import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',9545))

while True:
    u_input = input('>')
    if len(u_input) == 0:continue
    client.send(u_input.encode('UTF-8'))
    data_size = client.recv(1024).decode()
    client.send('OK'.encode())
    receive_size = 0
    print(data_size)
    print(type(data_size))
    while receive_size != int(data_size):
        data = client.recv(1024)
        receive_size += len(data)
        print(data.decode())
    else:
        print('total length is :',receive_size)
    
client.close()