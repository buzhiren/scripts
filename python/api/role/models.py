#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import sys
sys.path.append("..")
from utils.logtools import *
from utils.sqltools import *


class Role(object):
    def __init__(self,data):
        self.id = data

    def modify(self,data):
        self.res_dict = {}
        self.field = "role"
        self.newvalue = data["newvalue"]
        self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.result = self.new.UpdateData("dvd_role",{"id":self.id, "field":self.field, "newvalue":self.newvalue})
        print self.result
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
            self.res_dict = {"judge":"True","messg":""}
        return self.res_dict

    def query(self):
        self.res_list = []
        self.field_list = ["id","username","role"]
        self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.result = self.new.SelectData("dvd_role","")
        for m in self.result:
            self.res_dict = {}
            for n in range(len(self.field_list)):
                self.res_dict[self.field_list[n]] = m[n]
            self.res_list.append(self.res_dict)
        return self.res_list

    def drop(self):
        self.res_dict = {}
        self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.result = self.new.DeleteData("dvd_role",self.id)
        print self.result
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
            self.res_dict = {"judge":"True","messg":""}
        return self.res_dict



# a = {'username': 'lixiaoqiang', 'role': 'ordinary'}
# #"dvd_role",{"type":"role","content":"ordinary","newcon":"admin"})
#
# update dvd_role set role="admin" where id=1;
#
# he = Role("1")
# print he.drop()




