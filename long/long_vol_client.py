#!/usr/bin/env python


import socket
import json
import os
import hashlib
import cmd



class FtpClient(object):
    def __init__(self,name,passwd,quota):
        self.client = socket.socket()
        self.name = name
        self.passwd = passwd
        self.quota = quota
        self.current_dir = '/home/ftp/' + self.name
    
    def user_input(self):
        while True:
            u_input = input(self.current_dir + '>')
            if len(u_input.strip().split()) == 0: 
                continue
            elif len(u_input.strip().split()) == 1:
                cmd = u_input.strip().split()[0]
                filename = ''
            else:
                cmd = u_input.strip().split()[0]
                filename = u_input.strip().split()[1]
            info_msg = {
                'action':cmd,
                'filename':filename,
                'name':self.name,
                'passwd':self.passwd,
                'quota':quota
                }
            self.client.send(json.dumps(info_msg).encode())
            if hasattr(self, cmd):
                getattr(self, cmd)(info_msg)
            else:
                print("命令不存在!!!" % cmd)
                self.help()
    
    def cd(self,*args):
        self.current_dir = self.client.recv(1024).decode()
    
    def ls(self,*args):
        con_size = int(self.client.recv(1024).decode())
        self.client.send('ok'.encode())
        received_data = 0
        while received_data < con_size:
            result = self.client.recv(1024).decode()
            received_data += len(result)
            print(result,end='')
            
    def connect(self, ip, port):
        '''连接ftp服务器'''
        self.client.connect((ip, port))
    

username = 'zsc'
password = '123456'
quota = '10240'
f1 = FtpClient(username,password,quota)
f1.connect("localhost", 5580)
f1.user_input()