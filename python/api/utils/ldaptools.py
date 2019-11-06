#!/usr/bin/env python
# -*- coding: utf-8 -*-



import ldap


user = []
yunwei = {}

class findldap(object):
    def __init__(self,data):
        self.name = data["username"]
        self.pwd = data["password"]
        self.ldap_config = {
            'path' : "ldap://ldap-server.ops.vyohui.com:389",
            'base_dn' : "dc=davdian,dc=com",
            'user' : "cn=root,dc=davdian,dc=com",
            'passwd' : "dvd@1ppt"
        }

    def findname(self):
        try:
            self.con = ldap.initialize(self.ldap_config['path'])
            self.con.protocol_version = ldap.VERSION3
            self.con.simple_bind_s(self.ldap_config['user'], self.ldap_config['passwd'])
            self.searchScope = ldap.SCOPE_SUBTREE
            self.retrieveAttributes = None
            self.findname = 'cn=' + self.name
            self.result_id = self.con.search(self.ldap_config['base_dn'],self.searchScope,self.findname,self.retrieveAttributes)
            self.result_type, self.result_data = self.con.result(self.result_id)
        except Exception as e:
            print '连接失败',e

        if len(self.result_data) == 0:
            return False
        else:
            # cn user
            self.information, self.passwd = self.result_data[0]
            ldapPasswd = self.passwd['userPassword'][0]
            return True


# b = {"username":"lixiaoqiang", "password":"7x4yr9m2"}
# a = findldap(b)
# print a.findname()