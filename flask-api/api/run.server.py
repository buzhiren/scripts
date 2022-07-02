#!/usr/bin/env python
# -*- coding: utf-8 -*-



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask,request,render_template,flash,make_response,session,escape,redirect,url_for
from datetime import timedelta
import ConfigParser


# 读取 dvdcmdb.conf 配置文件的信息
config = ConfigParser.ConfigParser()
config.readfp(open("../conf/dvdcmdb.conf"))
run_port = config.get("conf","port")
run_ip = config.get("conf","ip")
run_debug = config.get("conf","log_debug")


# 导入 flask的Flask模块路由功能
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)





#  登录跳转login功能页面
@app.route('/')
def index():
  #return redirect(url_for('.static' , filename='html/login.html'))
  #return render_template('login.html')
  return "api"






# 用户api
from user import user
app.register_blueprint(user)


# # 资产相关api
from role import role
app.register_blueprint(role)


#
# # 资产相关api
from asset import asset
app.register_blueprint(asset)



# # 资产组相关api
from group_asset import group_asset
app.register_blueprint(group_asset)


if __name__ == '__main__':
  app.run(host='192.168.11.10',port=8000,debug=True)
