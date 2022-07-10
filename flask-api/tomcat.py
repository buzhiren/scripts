#!/usr/bin/env python
# coding: utf-8

from core import *

class Tomcat(Service, ClusterNode):
    '''tomcat服务
    实现Service, ClusterNode
    '''

    def __init__(self, service, check_file = 'ROOT/ok.html', check_url = '/ok.html'):
        '''
        service: 服务名 eg. apidoc.davdian.com
        check_file: eg. ROOT/ok.html
        check_url: eg. /ok.html
        '''
        self.base = '/home/work/%s' % service
        self.work_path = 'webapps'
        self.root_path = check_file.split('/')[0]

        config_file = '%s/conf/server.xml' % (self.base)
        config = self._parse_config_file(config_file)
        if not config:
            raise Exception('解析配置文件异常')
        self.address = config['address']
        self.port = config['port']
        self.check_file = '%s/%s/%s' % (self.base, self.work_path, check_file)
        self.check_url = 'http://%s:%s%s' % (config['address'], config['port'], check_url)

        Service.__init__(self, service, config['port'])
        ClusterNode.__init__(self, config['port'], self.check_file, self.check_url)
        pass

    def start(self, wait_time):
        '''启动服务
        wait_time为超时时间，非精确时间
        '''

        if self.is_alive():
            log.error('服务实例`%s`已存在, 无法启动多个实例' % self.service)
            return False

        command = 'su work -c "/home/service/tomcat/bin/start_tomcat.sh %s"' % (self.service)
        if not Shell.run(command):
            log.error('服务实例`%s`启动失败' % (self.service))
            return False
        return self.wait_alive(wait_time, True)

    def safe_stop(self, wait_time):
        '''正常停止服务(非kill)
        wait_time为超时时间，非精确时间
        '''

        command = 'su work -c "/home/service/tomcat/bin/stop_tomcat.sh %s -force"' % (self.service)
        Shell.run(command)
        return self.wait_alive(wait_time, False)

    def update(self, package):
        '''更新代码, 部署代码
        package war包
        '''

        extension = Shell.file_extension(package)
        command = 'rm -rf /home/work/%(service)s/webapps/%(path)s && unzip %(package)s -d /home/work/%(service)s/webapps/%(path)s' % {'package':package, 'service':self.service, 'path':self.root_path}
        return Shell.run(command)

    def _parse_config_file(self, config_file):
        '''解析配置文件'''

        import xml.etree.ElementTree as ET
        tree = ET.ElementTree(file = config_file)
        if not tree:
            return False

        connectors = tree.getroot().findall('Service/Connector')
        if not connectors:
            return False

        config = {'address':'127.0.0.1', 'work_path':'webapps', 'port':0}
        for connector in connectors:
            protocol = connector.get('protocol')
            if not protocol or 'HTTP' not in protocol.upper():
                continue
            config['port'] = connector.get('port')
            address = connector.get('address')
            if address:
                config['address'] = address
            break
        return config

if __name__ == '__main__':
    service = 'apidoc.davdian.com'
    tomcat = Tomcat(service)
    tomcat.offline()
    tomcat.stop(30)
    tomcat.update('/tmp/data/xxxx.war')
    tomcat.start(30)
    tomcat.online()
