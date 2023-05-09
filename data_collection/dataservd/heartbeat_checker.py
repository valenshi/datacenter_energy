# -*- coding: UTF-8 -*-
import subprocess
import xmlrpc.client
import csv
import threading
from time import sleep
import my_tool
from prettytable import PrettyTable

# 指定 RPC 服务器的地址和端口号
nodes = my_tool.get_nodes_ip()
vms = my_tool.get_vms()

def Ping(ip, name):
    try:
#        print('Ping', ip, name)
        server_url = "http://" + ip + ":9925/"
        proxy = xmlrpc.client.ServerProxy(server_url)
        result = proxy.ping()
    except Exception as e:
#        print(name+" is not ready :( ")
#        print(e)
        return False
#    print(name + "is ready :) ")
    return True

table = PrettyTable()
table.field_names = ["Hostname", "type", "ip", "status"]
table.align = "l"
for node in nodes:
    status = "DOWN"
    if Ping(node[1], node[0]):
        status = "UP"
    table.add_row([node[0], "compute", node[1], status])
for vm in vms:
    status = "DOWN"
    if Ping(vm[1], vm[0]):
        status = "UP"
    table.add_row([vm[0], "vm", vm[1], status])

print(table)
