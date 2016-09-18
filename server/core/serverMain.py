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
    init_dir = ''
    user_dir = ''
    current_dir = ''
#     current_dir = '/'.join(user_dir)
    server_path = ''
#     server_path = '/'.join(user_dir)
    def handle(self):
        count = 1
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                cmd_dic = json.loads(self.data.decode())
                self.username = cmd_dic['name']
                if count == 1:
                    self.init_dir = ['','home','ftp',self.username]
                    self.user_dir = ['','home','ftp',self.username]
                    self.current_dir = '/'.join(self.user_dir)
                    self.server_path = '/'.join(self.user_dir)
                    count += 1
                action = cmd_dic["action"]
                self.dir_path = cmd_dic['filename']
                if self.dir_path == '':
                    cmd_dic['filename'] = self.current_dir
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("err:", e)
                break
    
    def put(self, *args):
        '''接收客户端文件'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        user_quota = cmd_dic['quota']
        user_used_size = os.popen("ls -l /home/ftp/" + self.username +" | head -1 |awk '{print $2}' ").read()
        file_status_dic_recv = self.request.recv(1024).strip()
        file_status_dic = json.loads(file_status_dic_recv.decode())
        filesize = file_status_dic['file_size']
        
        if filesize + int(user_used_size) > int(user_quota):
            self.request.send('too large'.encode())
            return 'too large'
        filestatus = file_status_dic['quota_status']
        file_name = os.path.join(self.current_dir, filename)

        if os.path.isfile(file_name):
            f = open(file_name + ".new", "wb")
        else:
            f = open(file_name, "wb")
        self.request.send(b"200 ok") #返回状态码
        m = hashlib.md5()
        received_size = 0
        while received_size < filesize:
            data = self.request.recv(1024)
            m.update(data)
            f.write(data)
            received_size += len(data)
        else:
            file_md5 = m.hexdigest()
            self.request.send(file_md5.encode())
            print("\033[32;1m文件[%s]上传成功\033[;0m" % filename)
            
    
    def get(self, *args):
        '''发送文件给客户端'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        file_name = os.path.join(self.current_dir,filename)
        if os.path.isfile(file_name):
            file_size = os.stat(file_name).st_size
            self.request.send(str(file_size).encode())
            self.request.recv(1024)
            m = hashlib.md5()
            with open(file_name, "rb") as f:
                for line in f:
                    m.update(line)
                    self.request.send(line)
                else:
                    file_md5 = m.hexdigest()
                    self.request.send(file_md5.encode())
                    print("文件发送成功")
    
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
            print('456',dir_list)
        else:
            dir_list = dir_path.split('/')
        if not listContain.listContain(self.init_dir, dir_list):
            print('1111111111111111111111111111111')
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
        self.server_path = client_path
            
    def ls(self, *args):
        '''显示当前目录下所有文件'''

        cmd_dic = args[0]
        cmd_action = cmd_dic["action"]
        dir_path = cmd_dic["filename"]
#         print('ls:{}'.format(dir_path))
        path = os.popen(cmd_action + ' ' + '-l' + ' ' + dir_path).read()
        if len(path) == 0:
            path = 'command not found.\n'
        self.request.send(str(len(path.encode())).encode())
        self.request.recv(1024)
        self.request.sendall(path.encode())

    

    

    


def run():
    HOST, PORT = "localhost", 556
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
if __name__ == '__main__':
    run()
