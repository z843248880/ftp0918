#!/usr/bin/env python
# #coding:utf-8

import sys
import time



def view_bar(num, total):
    rate = num / total
    rate_num = int(rate * 100)
    r = '\r[%s%s]%d%%' % ("#" * num, " " * (100 - num), rate_num,)
    sys.stdout.write(r)
    sys.stdout.flush()


if __name__ == '__main__':
    a = 0.1
    for i in range(0, 101):
        time.sleep(0.1)
        view_bar(a, 10)
        a += 0.1






























# for i in range(1,11):
#     count + i = i
# for i in range(1,11):
#     print(count + i)
# 
# 
# rate = 0.95556 * 10 
# print(rate )









# 
# a = os.popen("ls -l /home/ftp/zsc | head -1 |awk '{print $2}' ").read()
# 
# if int(a) > 1024:
#     print('fdafadfs')























# """
# 查看文件夹下的所有文件及文件夹 join为拼接函数
# """
# def Look_File(path):
#   for root , dirs, files in os.walk(path, True):
#     print(root)     #主目录
#     for item in files: #主目录下的文件夹
#       print(os.path.join(root, item))
# """
# 计算文件夹 大小
# """   
# def FileSize(path):
#   size = 0
#   for root , dirs, files in os.walk(path, True):
#     size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
#     #目录下文件大小累加
#     return size
# if __name__ == '__main__':
#   Look_File("/home/ftp")
#   print(FileSize("/home/ftp"))


















# class Test(object):
#     name = '123'
#     def set(self):
#         self.name = '456'
#     def test(self):
#         print(self.name)
# 
#         
# t1 = Test()
# t1.set()
# t1.test()
































# cmd = 'get'
# filename = 'anme'
# 
# 
# 
# info_msg = {
#             'action':cmd,
#             'filename':filename
#                 }
# 
# def test1(info_msg):
#     print(info_msg['action'])
#     print(len(info_msg))
# 
# test1(info_msg)





















# 
# 
# import os
# 
# # user_dir = ['','home','ftp','zsc']
# # print('/'.join(user_dir))
# # str = '/home/ftp/zsc/2'
# # list1 = str.split('/')
# # print(list1)
# # print('/'.join(list1))
# # 
# # 
# # str1 = '../2/3'
# # if str1.startswith('../'):
# #     print(str1.strip('..'))
#     
# server_path = '/home/ftp/zsc'
# dir_path = '..'
# dir_path1 = '../'
# 
# server_list = server_path.split('/')
# server_list.pop()
# 
# 
# dir_list = dir_path.split('/')
# del dir_list[0]
# # print(dir_list)
# 
# server_list.extend(dir_list)
# print(server_list)
# # print('/'.join(server_list))
# 
# # print(n)
# 
# list1 = server_path.split('/')
# # print(list1)
# 
# # print(dir_path.split('/'))
# # print(dir_path1.split('/'))
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# # print(os.stat('/root/nohup.out').st_size)
# # 
# # data = os.popen('ls -l').read()
# #  
# # print(data)
