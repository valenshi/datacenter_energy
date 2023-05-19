# -*- coding: UTF-8 -*-
#!/usr/bin/env python3

import subprocess
import my_tool
from xmlrpc.server import SimpleXMLRPCServer

# 连接数据库
db = my_tool.MySQLTool(host='node1',username='ecm',password='123456',database='ecm')
result = db.select(table_name='nodedata',columns=['*'])


class API:
    def ping(self):
        return "200"
    def hostPower(self, nodeName):
        result = db.select(table_name="nodedata", columns=["power"], where="node_name = '"+nodeName+"'", order_by="timestamp DESC", limit=1)
        return result[0]['power']


# modify the ipaddr
# print(my_tool.get_host_ip())
server = SimpleXMLRPCServer((my_tool.get_host_ip(), 9926))
server.register_instance(API())
server.serve_forever()

