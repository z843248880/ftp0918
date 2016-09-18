#!/usr/bin/env python
#coding:utf-8


import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',9537))

current_dir = '/home/ftp/zsc'
while True:
    u_input = input(current_dir + '>')
    if len(u_input) == 0: continue
    client.send(u_input.encode())
    cmd = u_input.strip().split()[0]
#     path = u_input.strip().split()[1]
    if cmd == 'ls':

        con_size = int(client.recv(1024).decode())
        client.send('ok'.encode())
        received_data = 0
        while received_data < con_size:
            result = client.recv(1024).decode()
            received_data += len(result)
            print(result,end='')
    elif cmd == 'cd':
        current_dir = client.recv(1024).decode()
#         print('current_dir:{}'.format(current_dir))

client.close()



