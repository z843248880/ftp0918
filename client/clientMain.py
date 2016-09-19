#!/usr/bin/env python


import socket
import json
import os
import hashlib
import cmd
import sys
import time


def view_bar(num, total):
    rate = num / total
    rate_num = int(rate * 100)
    r = '\r[%s%s]%d%%' % ("#" * num, " " * (100 - num), rate_num,)
    sys.stdout.write(r)
    sys.stdout.flush()


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

                
    
    def put(self,info_msg):
        filename = info_msg['filename']
        if len(info_msg) > 1:
            if os.path.isfile(filename):
                file_size = os.stat(filename).st_size
                m = hashlib.md5()
                put_msg = {
                           "file_size": file_size,
                           "quota_status": True}
                self.client.send(json.dumps(put_msg).encode())
                server_response = self.client.recv(1024)  # 检测文件存在  返回配额限制
                print(server_response.decode())
                if server_response.decode() == 'too large':
                    print('the file is too large.')
                    return 'too large'
                with open(filename, "rb") as f:
#                     total_size = os.stat(filename).st_size
                    for line in f:
                        m.update(line)
                        self.client.send(line)
                    else:
                        local_file_md5 = m.hexdigest()
                        server_file_md5 = self.client.recv(1024)
                        print('local',local_file_md5)
                        print('server',server_file_md5.decode())
                        if local_file_md5 == server_file_md5.decode():
                            print("文件put成功^_^")
                        else:
                            print("文件put失败!!!")
            else:
                print("\033[31;1m文件 %s 不存在\033[;0m" % filename)
        else:
            print("cmd & filename")
    
    def get(self,info_msg):
        a = 0
        filename = info_msg['filename']
        file_size = int(self.client.recv(1024).decode())
        self.client.send('ok'.encode())
        received_size = 0
        if os.path.isfile(filename):
            f = open(filename + '.new','wb')
        else:
            f = open(filename,'wb')
        m = hashlib.md5()

        while received_size < file_size:
            if file_size - received_size > 1024:
                size = 1024
            else:
                size = file_size - received_size
            data = self.client.recv(size)
            m.update(data)
            received_size += len(data)
            f.write(data)
            rate = int((received_size / file_size) * 100)          
            if a == rate:
                time.sleep(0.1)
                view_bar(rate, 100)                
                a += 1

            
            
#             time.sleep(0.5)
#             if rate == a:
#                 print(int(rate))
#                 a += 1 
#                 print(rate,'   ',a)
            
        else:
            local_file_md5 = m.hexdigest()
            server_file_md5 = self.client.recv(1024)
            if local_file_md5 == server_file_md5.decode():
                print("文件下载成功^_^")
            else:
                print("文件下载失败 -_-!!!")

        
    
    
    
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
f1.connect("localhost", 555)
f1.user_input()
 
 



#         count1 = 0
#         count2 = 0
#         count3 = 0
#         count4 = 0
#         count5 = 0
#         count6 = 0
#         count7 = 0
#         count8 = 0
#         count9 = 0
#         count10 = 0

# if 1 < rate < 2:
#                 if count1 == 1:
#                     continue
#                 print('[#         ]10%')
#                 count1 = 1 
#             elif 2 < rate < 3:
#                 if count1 == 2:
#                     continue
#                 print('[##        ]20%')
#                 count1 = 2
#             elif 3 < rate < 4:
#                 if count1 == 3:
#                     continue
#                 print('[###       ]30%')
#                 count1 = 3
#             elif 4 < rate < 5:
#                 if count1 == 4:
#                     continue
#                 print('[####      ]40%')
#                 count1 = 4
#             elif 5 < rate < 6:
#                 if count1 == 5:
#                     continue
#                 print('[#####     ]50%')
#                 count1 = 5
#             elif 6 < rate < 7:
#                 if count1 == 6:
#                     continue
#                 print('[######    ]60%')
#                 count1 = 6
#             elif 7 < rate < 8:
#                 if count1 == 7:
#                     continue
#                 print('[#######   ]70%')
#                 count1 = 7
#             elif 8 < rate < 9:
#                 if count1 == 8:
#                     continue
#                 print('[########  ]80%')
#                 count1 = 8
#             elif 9 < rate < 10:
#                 if count1 == 9:
#                     continue
#                 print('[######### ]90%')
#                 count1 = 9
#             elif 10 <= rate <11:
#                 if count1 == 10:
#                     continue
#                 print('[##########]100%')
#                 count1 = 10   
    
    