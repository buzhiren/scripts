#!/usr/bin/env python
# -*- coding: utf-8 -*-



from models import *
from flask import Flask, jsonify, render_template, request, json,redirect
from user import user


@user.route('/v1/user/',methods=['POST'])
def user_login():
    asset_data = json.loads(request.get_data())
    case = User(asset_data)
    data = case.login()
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info