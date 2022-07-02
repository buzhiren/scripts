#!/usr/bin/env python
# -*- coding: utf-8 -*-




from flask import Flask, jsonify, render_template, request, json,redirect
from asset import asset
from models import *
sys.path.append("..")
from utils.jsontime import *


@asset.route('/v1/asset/',methods=['POST','GET'])
def increase():
    asset_data = json.loads(request.get_data())
    case = Asset(" ")
    data = case.Add_to(asset_data)
    info = json.dumps(data)
    return info



@asset.route('/v1/asset/all',methods=['GET'])
def query():
    case = Asset(" ")
    data = case.query()
    res_data = {
        "data": data,
    }
    info = json.dumps(data, cls=CJsonEncoder)
    return info



@asset.route('/v1/asset/<id>',methods=['PUT'])
def modify(id):
    asset_data = json.loads(request.get_data())
    case = Asset(id)
    data = case.modify(asset_data)
    info = json.dumps(data)
    return info




@asset.route('/v1/asset/<id>',methods=['DELETE'])
def delect(id):
    asset_data = json.loads(request.get_data())
    case = Asset(id)
    data = case.Delete()
    info = json.dumps(data)
    return info

@asset.route('/v1/ord_asset/',methods=['POST'])
def ord_apply():
    asset_data = json.loads(request.get_data())
    asset_data["ower"]="laowang"
    print asset_data
    case = Dmand(" ")
    data = case.apply(asset_data)
    res_data = {
        "data": data,
    }
    info = json.dumps(res_data)
    return info

@asset.route('/v1/ord_asset/<id>',methods=['POST'])
def ord_modify(id):
    case = Dmand("")
    data = case.modify(id)
    res_data = {
        "data": data,
    }
    info = json.dumps(res_data)
    return info
