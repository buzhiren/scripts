#!/usr/bin/python3
# -*-coding:utf-8 -*-


import logging

def log_print(log_data):
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    logging.info(log_data)


