#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, jsonify, render_template, request, json,redirect
from role import role
from models import *





@role.route('/v1/role/<id>',methods=['POST'])
def modify(id):
    role_data = json.loads(request.get_data())
    case = Role(id)
    data = case.modify(role_data)
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info



@role.route('/v1/role/all',methods=['GET'])
def query():
    case = Role(" ")
    data = case.query()
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info



@role.route('/v1/role/<id>',methods=['DELETE'])
def drop(id):
    case = Role(id)
    data = case.drop()
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info



# @asset.route('/v1/asset/all',methods=['GET'])
# def query():
#
#
#
#
#
#
# @asset.route('/v1/asset/<id>', methods=['PUT'])
# def modify(id):
#
#
# @asset.route('/v1/asset/<id>', methods=['DELETE'])
# def delect(id):