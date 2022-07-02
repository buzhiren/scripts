#!/usr/bin/python3
# -*-coding:utf-8 -*-


import sh
import re
import os
import time
import git
import json
import requests

from publicTools.log_pge import log_print
from publicTools.docker_cmd import DockerCmd, process_output

BASE_PATH = os.path.split(os.path.realpath(__file__))[0]


class SpringBootBuild:

    def __init__(self,arg_data):
        self.operation = arg_data['operation']
        self.env = arg_data['env']
        self.project_name = arg_data['project_name']
        self.git_branch = arg_data['branch']
        self.env_tag = arg_data['env_tag']
        self.time_tag = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.image_addr = "registry-vpc.cn-shenzhen.aliyuncs.com/lixiaoqiang-library"

        for line in open("%s/../code_data/spring_boot_info.txt" %BASE_PATH):
            if re.match(self.project_name, line):
                d = line.replace('\n', '')
                log_print(d)
                __project_name = d.split("|")[0]
                if __project_name == self.project_name:                
                    self.git_uri = d.split("|")[1]
                    self.git_home = d.split("|")[2]
                    self.package_file = d.split("|")[3]
                    self.name_space = d.split("|")[4]
                    self.domain = d.split("|")[5]
                break
            self.git_uri = None
        if not self.git_uri:
            log_print('项目信息未找到.')
            os._exit(4)

        if self.env_tag != None and self.env != "prod":
            self.deploy_name = "%s-%s-%s" %(self.env, self.project_name, self.env_tag)
            self.images_tag = "%s/%s:%s-%s" %(self.image_addr,self.project_name, self.env, self.env_tag)
        elif self.env_tag == None and self.env == "prod":
            self.deploy_name = "%s-%s" %(self.env, self.project_name)
            self.images_tag = "%s/%s:%s" %(self.image_addr, self.project_name, self.time_tag)
        else:
            print("env_tag 参数错误.")
            os._exit(4)

        if self.git_home != "pass":
            self.git_home_path = "%s/../work_space/%s/%s" %(BASE_PATH, self.deploy_name, self.git_home)
        else:
            self.git_home_path = "%s/../work_space/%s" %(BASE_PATH, self.deploy_name)


    def _git_info(self):
        _repo = git.Git()
        self.git_hash = _repo.log('-n','1','--pretty=format:%H')
        self.git_short_hash = _repo.log('-n','1','--pretty=format:%h')
        self.git_cn = _repo.log('-n','1','--pretty=format:%cn')
        self.git_message = _repo.log('-n','1','--pretty=format:%s')


    def git_code(self):
        log_print("开始git代码...")
        if self.operation == "rollback":
            log_print("不需要拉取代码.")
            return True

        if self.git_branch == None:
            self.git_branch = "master"
     
        sh.cd('%s/../work_space' %BASE_PATH)
        if os.path.exists(self.deploy_name):
            sh.rm('-fr', self.deploy_name)
        sh.git('clone', '-b', self.git_branch, self.git_uri, self.deploy_name, _out=process_output)
        sh.cd(self.git_home_path)
        self._git_info()

        log_print("开始mvn编译部分...")
        sh.mvn('clean', 'package', '-U', '-Dmaven.test.skip=true', _out=process_output)
        if not os.path.exists('target/%s' %self.package_file):
            log_print("mvn编译失败.")
            os._exit(4)
        log_print("mvn编译成功")
        sh.mkdir('docker-work')

    def image_create(self):
        log_print("开始docker image 构建部分...")
        _package_file_path = "%s/target/%s" %(self.git_home_path, self.package_file)
        self.docker_build_dir = '%s/docker-work/' %(self.git_home_path)
        _dorcker_file = '%s/../kubctl_template/springBoot/Dockerfile_template' %BASE_PATH

        # copy Dockerile, copy package_file
        sh.cd(self.docker_build_dir)
        sh.cp('-rp', _dorcker_file, 'Dockerfile')
        sh.cp('-rp', _package_file_path, self.package_file)

        # build images
        _docker_cmd = DockerCmd(self.images_tag, self.package_file, self.deploy_name, self.env)
        _docker_cmd.docker_buil()
        _docker_cmd.docker_push_pull()
        _img_tag = _docker_cmd.docker_image()
        if _img_tag != self.images_tag:
            log_print("镜像构建失败.")

        # run images
        #log_print("docker 测试运行检查, 等待20s...")
        #_http_code = _docker_cmd.docker_run()
        #if _http_code != 200:
        #    log_print("docker 运行失败,测试请求非200.")
        #log_print("docker 测试运行检查成功.")
        #_docker_cmd.docker_stop()

    def _deployment_var(self):
        _dep_env = os.environ.copy()
        try:
            _dep_env["NAME_SPACE"] = self.name_space
            _dep_env["DEPLOY_NAME"] = self.deploy_name
            _dep_env["IMAGE_ADDRESS"] = self.images_tag
            _dep_env["COMMIT_HASH"] = self.git_hash
        except NameError:
            log_print("yaml 变量为空.")
            os._exit(4)
        return _dep_env

    def _check_deployment(self, _deploy_name):
        _num = sh.wc(sh.kubectl('get', 'pod', '-l', 'app=%s' %_deploy_name,  '-n', self.name_space), '-l')
        self.num = int(_num.replace('\n',""))
        if self.num < 2:
            log_print("%s pod 不存在." %_deploy_name)
            os._exit(4)

    def deployment_update(self):
        if self.env == "prod":
            log_print("prod 环境暂时手动更新, 镜像: %s." %self.images_tag)
            return True    

        log_print("开始kubctl apply 部署")
        _deploy_file = '%s/../kubctl_template/springBoot/Deploy_template' %BASE_PATH
        
        sh.cd(self.docker_build_dir)
        _deploy_env = self._deployment_var()
        self._check_deployment(_deploy_env["DEPLOY_NAME"])

        sh.cp(_deploy_file, 'Deploy_template')
        _dep_file = sh.envsubst(sh.cat('Deploy_template'), _env=_deploy_env)
        _yaml_name = "%s.yaml" %_deploy_env["DEPLOY_NAME"]
        fo = open(_yaml_name,"w")
        for d_file in _dep_file:
            fo.write(d_file)
        fo.close()
        if not os.path.exists(_yaml_name):
            log_print("yaml文件创建失败.")
            os._exit(4)
        log_print("yaml文件创建成功,开始kubctl apply 更新...")
        sh.kubectl('apply', '-f', _yaml_name, _out=process_output)

    def _pod_check(self):
        _pod_number = sh.wc(sh.kubectl('get', 'pod', '-l', 'commitHash=%s' %self.git_hash, '-n', self.name_space), '-l')
        if int(_pod_number.replace('\n',"")) != self.num:
            return False
        return True

    def ding_ding(self, action=None):
        #url = "https://oapi.dingtalk.com/robot/send?access_token=ed2d5ef34f1c58d63ef5c4103e77d4e6a5c8eeb3df4534391ac472a0c9edb77e"
        url = "https://xxxxx"
        headers = {'Content-Type': 'application/json'}

        if action == "start":
            title = "服务部署-开始"
        elif action == "stop": 
            log_print("进入360s持续检测...")
            _count = 0
            while (_count < 1):
                time.sleep(120)
                _count = _count + 1
                if self._pod_check() == True:
                    title = "服务部署-成功"
                    break
        try:
            title
        except NameError as ex:
            log_print(ex)
            title = "服务部署-失败"


        text_content = "## %s\n\n>项目: %s\n\n>环境: %s-%s\n\n>域名: %s\n\n>镜像: %s\n\n>分支: %s\n\n>哈希: %s\n\n>描述: %s\n\n>提交: %s" %(title, self.project_name, self.env, self.env_tag, self.domain, self.images_tag, self.git_branch, self.git_short_hash, self.git_message, self.git_cn)
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text_content
            },
        }

        response  = requests.post(url, headers=headers, data=json.dumps(data))
        log_print(response.text)

    def end_action(self):
        pass


