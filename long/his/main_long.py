#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zhoujunlong
import socketserver
import json, os
import hashlib

base_dir = os.path.dirname(os.path.abspath(__file__))
status_dic = {
    "230": "login success",
    "250": "Ready to transfer files",
    "403": "no permissions",
    "530": "login fail",
    "550": "file is not exist",
    "570": "no enough space"
}


class MyTCPHandler(socketserver.BaseRequestHandler):

    def file_md5(self, filename):
        '''获取文件md5值'''
        m = hashlib.md5()
        with open(filename, "rb") as f:
            for line in f:
                m.update(line)
        return m.hexdigest()

    def handle(self):
        self.base_dir = base_dir
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print("{} write".format(self.client_address[0]))
                print(self.data.decode())
                cmd_dic = json.loads(self.data.decode())
                action = cmd_dic["action"]
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("\033[31;1merr:\033[;0m", e)
                break

    def ls(self, *args):
        '''显示当前目录下所有文件'''
        cmd_dic = args[0]
        cmd_action = cmd_dic["action"] + " " + self.base_dir
        print("cmd_action:", cmd_action)
        res = os.popen(cmd_action).read()
        print(res)
        self.request.send(res.encode())

    def pwd(self, *args):
        '''显示当前路径'''
        cmd_dic = args[0]
        cmd_action = cmd_dic["action"]
        res = os.popen(cmd_action).read()
        self.request.send(res.encode())

    def cd(self, *args):
        '''切换路径'''
        cmd_dic = args[0]
        print("cmd_dic", cmd_dic)
        raw_path = cmd_dic["raw_path"]
        print("raw_path: ", raw_path)
        change_path = cmd_dic["change_path"]
        if change_path == ".":
            new_path = raw_path
        elif change_path == "..":
            raw_path = set(raw_path)
            pop_path = set("/"+ self.base_dir.split("/")[-1])
            new_path = str(raw_path - pop_path)
        new_path = raw_path + "/" + change_path
        if os.path.exists(new_path):
            self.request.send(new_path.encode())
            self.base_dir = new_path
            print(self.base_dir)
        else:
            print("\033[31;1m路径不存在!!!\033[;0m")

    def put(self, *args):
        '''接收客户端文件'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        filesize = cmd_dic["file_size"]
        '''判断文件存不存在'''
        if os.path.isfile(filename):
            f = open(filename + ".new", "wb")
        else:
            f = open(filename, "wb")
        self.request.send(b"200 ok") #返回状态码
        received_size = 0
        while received_size < filesize:
            data = self.request.recv(1024)
            f.write(data)
            received_size += len(data)
        else:
            file_md5 = self.file_md5(filename)
            self.request.send(file_md5.encode())
            print("\033[32;1m文件[%s]上传成功\033[;0m" % filename)

    def get(self, *args):
        '''发送文件给客户端'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        if os.path.isfile(filename):
            status = "250: "+status_dic["250"]
            print(status)
            self.request.send(status.encode())
            self.request.recv(1024)
            file_size = os.stat(filename).st_size
            self.request.send(str(file_size).encode())
            self.request.recv(1024)
            with open(filename, "rb") as f:
                for line in f:
                    self.request.send(line)
                else:
                    file_md5 = self.file_md5(filename)
                    self.request.send(file_md5.encode())
                    print("\033[32;1m文件发送成功\033[;0m")
        else:
            status = "570: "+status_dic["570"]
            self.request.send(status.encode())

def run():
    HOST, PORT = "localhost", 5566
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
if __name__ == '__main__':
    run()