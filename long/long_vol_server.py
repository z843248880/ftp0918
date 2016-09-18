#!/usr/bin/env python

import socketserver
import json,os,sys
import hashlib


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from core import listContain


class MyTCPHandler(socketserver.BaseRequestHandler):
    username = ''
    dir_path = ''
    init_dir = ['','home','ftp',username]
    user_dir = ['','home','ftp',username]
    current_dir = '/'.join(user_dir)
    server_path = '/'.join(user_dir)
    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                cmd_dic = json.loads(self.data.decode())
                self.username = cmd_dic['name']
                print(self.username + '123123123213')
                self.init_dir = ['','home','ftp',self.username]
                self.user_dir = ['','home','ftp',self.username]
                action = cmd_dic["action"]
                
                if self.dir_path == '':
                    cmd_dic['filename'] = self.current_dir
                print('fdsfad',cmd_dic['filename'])
                self.dir_path = cmd_dic['filename']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("err:", e)
                break
    
    def cd(self, *args):
        '''切换路径'''
        cmd_dic = args[0]
        cmd = cmd_dic["action"]
        dir_path = cmd_dic['filename']
        if not dir_path.startswith('/') and not dir_path.startswith('..'):
            dir_list = (self.server_path + '/' + dir_path).split('/')
        elif dir_path.startswith('..'):
            server_path_list = self.server_path.split('/')
            server_path_list.pop()
            dir_path_list = dir_path.split('/')
            del dir_path_list[0]
            server_path_list.extend(dir_path_list)
            dir_list = server_path_list
        else:
            dir_list = dir_path.split('/')
        if not listContain.listContain(self.init_dir, dir_list):
            client_path = '/'.join(self.init_dir)
            self.current_dir = client_path
        else:
            if dir_path.startswith('/'):
                client_path = dir_path
                self.current_dir = client_path
            elif dir_path.startswith('../'):
                self.user_dir.pop()
                client_path = '/'.join(self.user_dir) + dir_path.strip('..')
                self.current_dir = client_path
            else:
                if dir_path == '..':
                    self.user_dir.pop()
                else:
                    self.user_dir.append(dir_path)
                client_path = '/'.join(self.user_dir)
                self.current_dir = client_path
        self.request.send(client_path.encode())
        self.dir_path = client_path
        print('test3:',self.dir_path)
        self.server_path = client_path
            
    def ls(self, *args):
        '''显示当前目录下所有文件'''

        cmd_dic = args[0]
        cmd_action = cmd_dic["action"]
        dir_path = cmd_dic["filename"]
        print('ls:{}'.format(dir_path))
        path = os.popen(cmd_action + ' ' + '-l' + ' ' + dir_path).read()
        if len(path) == 0:
            path = 'command not found.\n'
        self.request.send(str(len(path.encode())).encode())
        self.request.recv(1024)
        self.request.sendall(path.encode())
        
def run():
    HOST, PORT = "localhost", 5580
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
if __name__ == '__main__':
    run()