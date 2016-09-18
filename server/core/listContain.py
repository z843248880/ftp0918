#!/usr/bin/env python
#coding:utf-8


def listContain(list1,list2):
    if len(list1) > len(list2):
        return False
    else:
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        else:
            return True

