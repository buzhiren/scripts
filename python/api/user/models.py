#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import sys
sys.path.append("..")
from utils.logtools import *
from utils.sqltools import *
from utils.ldaptools import *


class User(object):
    def __init__(self,data):
        self.name = data['username']
        self.pwd = data['password']

    def login(self):
        # self.input = { self.name : self.pwd  }
        # self.auth = findldap(self.input)
        # self.auth_data = self.auth.findname
        self.auth_data = True
        if self.auth_data != True:
            self.judge = "False"
            self.messg = "用户或密码不对"
        else:
            self.judeg = "True"
            self.messg = " "
            self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", "3306", "dvd_cmdb")
            self.res = self.new.SelectData("dvd_role", "")
            for n in self.res:
                if self.name in n:
                    self.juname = "True"
                    break
                else:
                    self.juname = "False"

            #  初次登入加入角色
            if self.juname != "True":
               self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", "3306", "dvd_cmdb")
               self.inser = self.new.InsertData("dvd_role",{"username":self.name,"role":"ordinary"})
               if self.inser == "True":
                   self.messg = "角色加入成功"
               else:
                   self.messg = "角色加入失败"


            #  返回角色信息
            self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", "3306", "dvd_cmdb")
            self.role = self.inser = self.new.SelectData("dvd_role",{"field":"username","content":self.name})
            self.returninfo = { "judge":self.judeg, "messg":self.messg, "role":self.role[0][2]}
            return self.returninfo

# ki = {"username":"lixiaoqiang", "password":"7x4yr9m2"}
# bb = User(ki)
# print bb.login()



