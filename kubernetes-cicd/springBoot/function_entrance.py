#!/usr/bin/python3
# -*-coding:utf-8 -*-


from springBoot.build_pge import SpringBootBuild

def spring_boot_implement(arg_data):
    s_build = SpringBootBuild(arg_data)
    s_build.git_code()
    s_build.ding_ding("start")
    s_build.image_create()
    s_build.deployment_update()
    s_build.ding_ding("stop")

