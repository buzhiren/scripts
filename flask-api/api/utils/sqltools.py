#!/usr/bin/env python
# -*- coding: utf-8 -*-


#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mysql.connector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Mysqltools(object):
    def __init__(self,host,user,pwd,port,dbname):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.dbname = dbname
	print self.port
        self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            port = self.port,
            password = self.pwd,
            database = self.dbname,
        )


    def InsertData(self,tablename,data):
        self.data = data
        self.tablename = tablename
        self.key = []
        self.val = []
        for i in range(len(self.data)):
            self.key.append(self.data.keys()[i])
            self.val.append(str(self.data.values()[i]))
        self.key1 = ",".join(self.key)
        self.val1 = "' , '".join(self.val)
        self.sql = "insert into " + self.tablename + "("+ self.key1 +")values('" +self.val1+ "');"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql)
            self.conn.commit()
            self.conn.close()
            return "True"
        except mysql.connector.Error as e:
            return ('insert datas error!{}'.format(e))

    def UpdateData(self,tablename,data):
        self.tablename = tablename
        self.id = data["id"]
        self.field = data["field"]
        self.newvalue = data["newvalue"]
        self.sql = "update " + self.tablename + " set " + self.field + "='" +self.newvalue+ "' where id=" +self.id+ ";"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql)
            self.conn.commit()
            self.conn.close()
            return "True"
        except mysql.connector.Error as e:
            return ('update datas error!{}'.format(e))


    def SelectData(self,tablename,data):
        if data == "":
            self.sql = "select * from " +tablename+";"
        elif len(data) == 1:
            self.sql = "select * from " +tablename+ " where " +data["field"]+  ";"
        else:
            self.type = data["field"]
            self.content = data["content"]
            self.sql = "select * from " +tablename+ " where " +self.type+ "='" +self.content+  "';"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchall()
            self.tup_data = self.data
            self.conn.close
            return self.tup_data
        except mysql.connector.Error as e:
            return ('select datas error!{}'.format(e))

    def SelectColumn(self,tablename,data):
        self.type = data["type"]
        self.tablename = tablename
        self.sql = "select " +self.type+ " from "  +self.tablename+";"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql)
            self.data = self.cursor.fetchall()
            self.conn.close
            return self.data
        except mysql.connector.Error as e:
            return ('select datas error!{}'.format(e))

    def DeleteData(self,tablename,id):
        self.tablename = tablename
        self.id = id
        self.sql = "delete from " + self.tablename+ " where id=" +self.id+ ";"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql)
            self.conn.commit()
            self.conn.close
            return "True"
        except mysql.connector.Error as e:
            return ('select datas error!{}'.format(e))






