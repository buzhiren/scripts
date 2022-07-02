#!/usr/bin/python3
# -*-coding:utf-8 -*-


import argparse
import sys

from publicTools.log_pge import log_print
from springBoot.function_entrance import spring_boot_implement
from nodeJs.function_entrance import node_js_implement

def arg_info():
    parser = argparse.ArgumentParser(description='Automated Deployment')
    parser.add_argument('-o', '--operation', metavar='deploy|RollBACK', type=str, choices=['deploy','rollback'], required=True, 
                        help='deploy rollback action')
    
    parser.add_argument('-e', '--env', metavar='dev|fat|uat|pro', type=str, choices=['test','fat','uat','pro'], required=True,
                        help='Acting on the environment')
    
    parser.add_argument('-n', '--project_name', metavar='apiserver...', type=str, required=True,
                        help='code name')
    
    parser.add_argument('-c', '--confirm', metavar='apiserver...', type=str, required=True,
                        help='code name confirm')

    parser.add_argument('-b', '--branch', metavar='dev/master.', type=str,
                        help='git branch')

    parser.add_argument('-t', '--env_tag', metavar='01|02|03|04', type=str,
                        help='env tag')        

    parser.add_argument('-l', '--language', metavar='node|spingboot', type=str, choices=['nodejs','spingboot'], required=True,
                        help='code language')

    _arg_list = parser.parse_args()
    _arg_dict = {}
    _arg_dict['operation'] = _arg_list.operation
    _arg_dict['env'] = _arg_list.env  
    _arg_dict['project_name'] = _arg_list.project_name
    _arg_dict['confirm'] = _arg_list.confirm
    _arg_dict['branch'] = _arg_list.branch
    _arg_dict['env_tag'] = _arg_list.env_tag
    _arg_dict['language'] = _arg_list.language
   
    if _arg_dict['project_name'] != _arg_dict['confirm']:
        log_print("程序名称输入不一致")
        sys.exit(4)

    log_print(_arg_dict)
    return _arg_dict
    


if __name__ == '__main__':
    arg_data = arg_info()
    language = arg_data["language"]
    if language == "spingboot":
        spring_boot_implement(arg_data)
    elif language == "node":
        node_js_implement(arg_data)

