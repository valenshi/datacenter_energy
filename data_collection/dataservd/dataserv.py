# -*- coding: UTF-8 -*-
#!/usr/bin/env python3

import subprocess
import my_tool
from xmlrpc.server import SimpleXMLRPCServer
class Server:
    def ping(self):
        return "200"
    def hostcollector(self):
        result = subprocess.run('~/datacenter_energy/data_collection/sysstat/hostcollector.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode('utf-8')
        else:
            return result.stderr.decode('utf-8')
    def powercollector(self):
        result = subprocess.run('~/datacenter_energy/data_collection/ipmi/powercollector.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode('utf-8')
        else:
            return result.stderr.decode('utf-8')

    def vmcollector(self):
        result = subprocess.run('~/datacenter_energy/data_collection/sysstat/vmcollector.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode('utf-8')
        else:
            return result.stderr.decode('utf-8')

    def podcollector(self):
        result = subprocess.run('~/datacenter_energy/data_collection/sysstat/podcollector.sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return result.stdout.decode('utf-8')
        else:
            return result.stderr.decode('utf-8')

# modify the ipaddr

server = SimpleXMLRPCServer((my_tool.get_host_ip(), 9925))
server.register_instance(Server())
server.serve_forever()

