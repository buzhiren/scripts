#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import sys
sys.path.append("..")
from utils.logtools import *
from utils.sqltools import *
from asset.models import *




class Group_Asset(object):
    def __init__(self,data):
        self.id = data


    def increase(self,data):
        self.data = data
        self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.result = self.new.InsertData("group_asset",self.data)
        if self.result != "True":
            self.res_dict = {"judge":"False","messg":self.result}
        elif self.result == "True":
            self.res_dict = {"judge":"True","messg":""}
        return self.res_dict


    def query(self):
        self.field_list = ["id","group_name"]
        self.res_list = [ ]
        self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.result = self.new.SelectData("group_asset", "")
        for m in self.result:
            self.res_dict = {}
            for n in range(len(self.field_list)):
                self.res_dict[self.field_list[n]] = m[n]
            self.res_list.append(self.res_dict)
        return self.res_list





class relevance(Group_Asset,Asset):
    def rele(self,data):
        self.g_number = data["asset_num"]
        self.group_name = data["grup_ast"]


        # 获取资产和资产组数据
        self.group_result = Group_Asset.query(self)
        for n in range(len(self.group_result)):
            if self.group_name == self.group_result[n]['group_name']:
                self.group_id = self.group_result[n]['id']
                break
            else:
                self.group_id = "False"
        self.asset_result = Asset.query(self)
        for n in range(len(self.asset_result)):
            if self.g_number == self.asset_result[n]['g_number']:
                self.asset_id = self.asset_result[n]['id']
                break
            else:
                self.asset_id = "False"
        # 添加资产
        self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.asset_relation = self.new.SelectData("asset_relation","")
        self.request_dict = {self.asset_id: self.group_id}
        if self.group_id == "False":
            self.res_info = {"judge": "False", "messg": "资产组不存在"}
            return self.res_info
        elif self.asset_id == "False":
            self.res_info = {"judge": "False", "messg": "资产不存在"}
            return self.res_info
        else:
            self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
            self.rele_result = self.new.InsertData("asset_relation",{"asset_group_id":self.group_id,"asset_id":self.asset_id})
            self.res_info = {"judge": "True", "messg": " "}
            return self.res_info
        return self.res_info

    def asset_query(self,data):
        self.g_number = data
	self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.asset_info = self.new.SelectData("cmdb_tmp_goods",{"field":"g_number","content":self.g_number})
	self.asset_id = str(self.asset_info[0][0])
        self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.group_asset_info = self.new.SelectData("asset_relation","")
	for n in self.group_asset_info:
	  if n[1] == self.asset_id:
	    self.group_asset_id = n[2]
	    break
	self.new = Mysqltools("192.168.193.10", "dvd_cmdb", "123456", 3306, "dvd_cmdb")
        self.group_asset = self.new.SelectData("group_asset",{"field":"id","content":self.group_asset_id})
	self.res_dict = {"messg":self.group_asset[0][1]} 
	return self.res_dict


# asset_data = { "grup_ast":"技术部","asset_num": "buHid",}
# case = relevance(" ")
# data = case.rele(asset_data)
#
#
# print data

# #  查看资产或者资产组是否存在
# if self.group_id == "False":
#     self.res_info = {"judge": "False", "messg": "资产组不存在"}
#     return self.res_info
# elif self.asset_id == "False":
#     self.res_info = {"judge": "False", "messg": "资产不存在"}
#     return self.res_info

# for n in range(len(self.asset_relation)):
#     self.rela_dict = {}
#     self.rela_dict[self.asset_relation[n][1]] = self.asset_relation[n][2]
#     print self.rela_dict[self.asset_relation[n][1]]
#     if self.request_dict[self.asset_id] == self.rela_dict[self.asset_relation[n][1]]:
#         self.res_info = {"judge": "True", "messg": "配置过"}
#         return self.res_info



















