#!/usr/bin/python3
# -*-coding:utf-8 -*-

import sh
import time


def process_output(line):
        print(line.replace('\n', ''))


class DockerCmd():
    
    def __init__(self, images_tag, package_file, deploy_name, env):
        self.images_tag = images_tag
        self.package_file = package_file
        self.deploy_name = deploy_name
        self.env = env
        
    def docker_buil(self):
        sh.docker('build', '-t', self.images_tag, '-f', 'Dockerfile', '--build-arg', 'deploy_env=%s' %self.env, '--build-arg', 'code_name=%s' %self.package_file, '.', _out=process_output)

    def docker_image(self):
        _images_info = sh.docker('images', '--filter=reference=%s' %self.images_tag)
        _img = list(_images_info)[1]
        _img_list = list(filter(None,_img.split(" ")))
        _img_tag = "%s:%s" %(_img_list[0], _img_list[1])
        return _img_tag

    def docker_run(self):
        _ps_info = sh.docker('ps', '-a', '--filter=name=%s' %self.deploy_name)
        _ps_list = list(_ps_info)
        if len(_ps_list) > 1:
            sh.docker('stop', self.project_name)
            sh.docker('rm', self.project_name)

        sh.docker('run', '-itd', '--name=%s' %self.deploy_name, self.images_tag)
        time.sleep(15)
        _curl_cmd = "curl -sIL -w %{http_code} -o /dev/null http://localhost:8080/"
        _http_code = sh.docker('exec', '-i', self.deploy_name, '/bin/bash', '-c', _curl_cmd)
        return _http_code

    def docker_stop(self):
        sh.docker('stop', self.deploy_name)
        sh.docker('rm', self.deploy_name)

    def docker_push_pull(self):
        sh.docker('push','-q', self.images_tag, _out=process_output)
        time.sleep(1)
        sh.docker('rmi', self.images_tag, _out=process_output)
        time.sleep(2)
        sh.docker('pull', '-q', self.images_tag, _out=process_output)


