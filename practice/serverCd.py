#!/usr/bin/env python
#coding:utf-8

import socket,os
from practice import listContain

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',9537))
server.listen()

username = 'zsc'

init_dir = ['','home','ftp',username]

user_dir = ['','home','ftp',username]
current_dir = '/'.join(user_dir)
server_path = '/'.join(user_dir)

while True:
    conn,addr = server.accept()
    while True:
        data = conn.recv(10240).decode()
        if not data:break
        try:
            cmd = data.strip().split()[0]
            dir_path = data.strip().split()[1]
        except IndexError as e:
            dir_path = current_dir
        if cmd == 'cd':
            if not dir_path.startswith('/') and not dir_path.startswith('..'):
                dir_list = (server_path + '/' + dir_path).split('/')
            elif dir_path.startswith('..'):
                server_path_list = server_path.split('/')
                server_path_list.pop()
                dir_path_list = dir_path.split('/')
                del dir_path_list[0]
                server_path_list.extend(dir_path_list)
                dir_list = server_path_list
            else:
                dir_list = dir_path.split('/')
            if not listContain.listContain(init_dir, dir_list):
                client_path = '/'.join(init_dir)
                current_dir = client_path
            else:
                if dir_path.startswith('/'):
                    client_path = dir_path
                    current_dir = client_path
                elif dir_path.startswith('../'):
                    user_dir.pop()
                    print(user_dir)
                    print(dir_path)
                    client_path = '/'.join(user_dir) + dir_path.strip('..')
                    current_dir = client_path
                else:
                    if dir_path == '..':
                        user_dir.pop()
                    else:
                        user_dir.append(dir_path)
                    client_path = '/'.join(user_dir)
                    current_dir = client_path
#             print('client_dir:{}'.format(client_dir))
            

            conn.send(client_path.encode())
            server_path = client_path
                
            
        if cmd == 'ls':      
            print('ls:{}'.format(dir_path))
            path = os.popen(cmd + ' ' + '-l' + ' ' + dir_path).read()
            if len(path) == 0:
                path = 'command not found.\n'
            conn.send(str(len(path.encode())).encode())
            conn.recv(1024)
            conn.sendall(path.encode())
server.close()