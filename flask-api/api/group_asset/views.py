#!/usr/bin/env python
# -*- coding: utf-8 -*-




from flask import Flask, jsonify, render_template, request, json,redirect
from group_asset import group_asset
from models import *
sys.path.append("..")
from utils.jsontime import *


@group_asset.route('/v1/group_asset/',methods=['POST'])
def increase():
    asset_data = json.loads(request.get_data())
    case = Group_Asset(" ")
    data = case.increase(asset_data)
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info

@group_asset.route('/v1/group_asset/all',methods=['GET'])
def query():
    case = Group_Asset(" ")
    data = case.query()
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info


@group_asset.route('/v1/group_asset/relation',methods=['POST'])
def relation():
    asset_data = json.loads(request.get_data())
    case = relevance(" ")
    data = case.rele(asset_data)
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info


@group_asset.route('/v1/group_asset/<id>',methods=['GET'])
def asset_query(id):
    case = relevance(" ")
    data = case.asset_query(id)
    fask = {
        "data":data
    }
    info = json.dumps(fask)
    return info
