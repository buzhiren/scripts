#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import sys
sys.path.append("..")
from utils.logtools import *
from utils.sqltools import *




class Asset(object):
    def __init__(self,data):
        self.id = data
        # self.field = data["field"]
        # self.newvalue = data["newvalue"]



    def  Add_to(self,data):
        self.res_dict = {}
        self.data = data
        self.new = Mysqltools("xxxxxxx", "cmdb", "123456", 3306, "cmdb")
        self.result = self.new.InsertData("tmp_goods",self.data)
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
            self.res_dict = {"judge":"True","messg":""}
        return self.res_dict



    def Delete(self):
        self.res_dict = {}
        self.new = Mysqltools("xxxxxx", "cmdb", "123456", 3306, "cmdb")
        self.result = self.new.DeleteData("cmdb_tmp_goods",self.id)
	# self.new.UpdateData("mdb_tmp_goods",{"id":self.id,"field":self.field,"newcon":"未使用"})
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
            self.res_dict = {"judge":"True","messg":""}
        return self.res_dict

    def modify(self,data):
        self.res_dict = {}
        self.field = data["field"]
        self.newvalue = data["newvalue"]
        self.new = Mysqltools("xxxxxx", "cmdb", "123456", 3306, "cmdb")
        self.result = self.new.UpdateData("cmdb_tmp_goods",{"id":self.id, "field":self.field, "newvalue":self.newvalue})
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
            self.res_dict = {"judge":"True","messg":""}
        return self.res_dict

    def query(self):
        self.field_list = ["id","g_number","g_type","g_brand","g_price","g_owner","pur_time","begin_time","end_time","g_state"]
        self.res_list = [ ]
        self.new = Mysqltools("xxxxxxx", "cmdb", "123456", 3306, "cmdb")
        self.result = self.new.SelectData("cmdb_tmp_goods", "")

        for m in self.result:
            self.res_dict = {}
            for n in range(len(self.field_list)):
                self.res_dict[self.field_list[n]] = m[n]
            self.res_list.append(self.res_dict)
        return self.res_list



class Dmand(object):
    def __init__(self,data):
        self.data = data

    def apply(self,data):
        self.res_dict = {}
        self.data = data
        self.new = Mysqltools("xxxxxxx", "cmdb", "123456", 3306, "cmdb")
        self.result = self.new.InsertData("demand",self.data)
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
            self.res_dict = {"judge":"True","messg":"添加成功"}
        return self.res_dict

    def modify(self,data):
        self.id = data
        self.new = Mysqltools("xxxxx", "cmdb", "123456", 3306, "cmdb")
        self.info = self.new.SelectData("cmdb_tmp_goods",{"field":"g_number","content":self.id})
        self.new = Mysqltools("xxxxxx", "cmdb", "123456", 3306, "cmdb")
        self.result = self.new.UpdateData("cmdb_tmp_goods",{"field":"g_state","newvalue":"未使用","id":str(self.info[0][0])})
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
             self.res_dict = {"judge":"True","messg":"退回成功"}
        return self.res_dict





