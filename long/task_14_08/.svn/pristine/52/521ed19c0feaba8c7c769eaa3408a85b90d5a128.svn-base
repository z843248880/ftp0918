#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zhoujunlong
import socketserver
import json, os,sys
import hashlib

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
status_dic = {
    "230": "login success",
    "250": "Ready to transfer files",
    "403": "no permissions",
    "530": "login fail",
    "550": "file is not exist",
    "570": "no enough space"
}


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.base_dir = os.path.join(base_dir,"data")
        self.name = ""
        self.path = ""
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print("{} write".format(self.client_address[0]))
                print(self.data)
                cmd_dic = json.loads(self.data.decode())
                action = cmd_dic["action"]
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("\033[31;1merr:\033[;0m", e)
                break

    def auth(self, name, passwd):
        account_file = "%s/data/users/%s.json" % (base_dir, name)
        try:
            while True:
                    if os.path.isfile(account_file):
                        with open(account_file) as f:
                            account_data = json.load(f)
                            if account_data["password"] == passwd:
                                self.name = name
                                self.path = os.path.join(self.base_dir, self.name)
                                return True
                                break

                            else:
                                return False
                    else:
                        return False
        except Exception as e:
            print("err:", e)

    def acc_login(self, *args):
        cmd_dic = args[0]
        user_name = cmd_dic["user_name"]
        user_passwd = cmd_dic["user_passwd"]
        auth = self.auth(user_name, user_passwd)
        self.request.send(str(auth).encode())

    def ls(self, *args):
        '''显示当前目录下所有文件'''
        cmd_dic = args[0]
        cmd_action = cmd_dic["action"] +" "+self.path
        res = os.popen(cmd_action).read()
        if len(res) == 0:
            res = "\n"
        self.request.send(res.encode())

    def pwd(self, *args):
        '''显示当前路径'''
        self.request.send(self.path.encode())

    def cd(self, *args):
        '''切换路径'''
        cmd_dic = args[0]
        raw_path = cmd_dic["raw_path"]
        change_path = cmd_dic["change_path"]
        if change_path == ".":
            new_path = raw_path
        elif change_path == "..":
            pop_path = "/"+ raw_path.split("/")[-1]
            if pop_path == "/"+self.name:
                new_path = raw_path
            else:
                new_path =raw_path[:-len(pop_path)] 
        else:
            new_path = os.path.join(raw_path, change_path)
        if os.path.isdir(new_path):
            self.path = new_path
            self.request.send(new_path.encode())
            print(self.path)
        else:
            self.request.send("路径不存在!!!".encode())
            print("\033[31;1m路径不存在!!!\033[;0m")

    def put(self, *args):
        '''接收客户端文件'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        filesize = cmd_dic["file_size"]
        file_name = os.path.join(self.path, filename)
        '''判断文件存不存在'''
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
        file_name = os.path.join(self.path,filename)
        if os.path.isfile(file_name):
            status = "250: "+status_dic["250"]
            self.request.send(status.encode())
            self.request.recv(1024)
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
                    print("\033[31;1m文件发送成功\033[;0m")
        else:
            status = "550: "+status_dic["550"]
            self.request.send(status.encode())


def run():
    HOST, PORT = "localhost", 5555
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
if __name__ == '__main__':
    run()
