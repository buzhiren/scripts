#!/bin/python3
# coding:utf-8


import logging
import requests
import json


def logInfo(log_data):
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='logs/upload.log', level=logging.DEBUG, format=LOG_FORMAT)

    logging.info(log_data)


def dingDing(md5,file_name):
    url = "https://oapi.dingtalk.com/robot/send?access_token=ed2d5ef34f1c58d63ef5c4103e77d4e6a5c8eeb3df4534391ac472a0c9edb77e"
    headers = {'Content-Type': 'application/json'}

    data = {
        "at": {
            "atMobiles":[
                "15201109320","18611631775","13809890030"
            ],
        "isAtAll": False
        },
        "text": {
        "content":"上传文件通知\nMD5: %s \nFileName: %s" %(md5, file_name)
        },
        "msgtype":"text"
    }

    response  = requests.post(url, headers=headers, data=json.dumps(data))
    logInfo(response.text)


