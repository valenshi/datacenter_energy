# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
import configparser
import os
import my_tool
from xmlrpc.server import SimpleXMLRPCServer

# 连接数据库
db = my_tool.MySQLTool(host='node1',username='ecm',password='123456',database='ecm')
result = db.select(table_name='nodedata',columns=['*'])

#读取配置文件
conf_url = os.path.expanduser("~/datacenter_energy/config/dataserv.conf")

class API:
    def ping(self):
        return "200"
    def hostPower(self, nodeName):
        # print("enter hostPower()!!!")
        result = db.select(table_name="nodedata", columns=["power"], where="node_name = '"+nodeName+"'", order_by="timestamp DESC", limit=1)
        # print("hostPower success!!!, power is ", result[0]['power'])
        return str(result[0]['power'])
    
    def energyCost(self, nodeName):
        try:
            # 读取 dataserv.conf 文件
            conf = configparser.ConfigParser()
            conf.read(conf_url)

            # 获取 [energyCost] 部分的列表项
            energy_cost = conf.items('energyCost')
            dict_nodes = dict(energy_cost)
            return dict_nodes.get(nodeName)
        except:
            return "Error: Failed to load dataserv.conf file"
    
    def powerLimit(self ,nodeName):
        try:
            # 读取 dataserv.conf 文件
            conf = configparser.ConfigParser()
            conf.read(conf_url)

            # 获取 [powerLimit] 部分的列表项
            power_limit = conf.items('powerLimit')
            dict_nodes = dict(power_limit)
            # print(dict_nodes)
            return dict_nodes.get(nodeName)
        except:
            return "Error: Failed to load dataserv.conf file"

# modify the ipaddr
# print(my_tool.get_host_ip())
server = SimpleXMLRPCServer((my_tool.get_host_ip(), 9926))
server.register_instance(API())
server.serve_forever()
