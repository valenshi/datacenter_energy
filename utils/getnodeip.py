# -*- coding: UTF-8 -*-
import configparser
import socket
conf_url = "/root/datacenter_energy/config/dataserv.conf"
def get_vms():
    #让gpt写
    """
    获取所有节点及其对应的IP地址
    """

    try:
        # 读取 dataserv.conf 文件
        conf = configparser.ConfigParser()
        conf.read(conf_url)

        # 获取 [hosts] 部分的列表项
        vms = conf.items('vms')
        return vms

    except:
        print("Error: Failed to load dataserv.conf file")
    return
def get_host_ip():
    """
    获取当前主机的 IP 地址
    """

    # 获取当前主机名
    host_name = socket.gethostname()
    try:
        # 读取 dataserv.conf 文件
        conf = configparser.ConfigParser()
        conf.read(conf_url)

        # 获取 [hosts] 部分的列表项
        nodes_ip = conf.items('hosts')
        nodes_ip += conf.items('vms')
        # 找到当前主机名对应的 IP 地址
        for node, ip in nodes_ip:
            if node == host_name:
                return ip

    except:
        print("Error: Failed to load dataserv.conf file")
# 测试函数
# print(get_host_ip())

def get_nodes_ip():
    """
    获取所有节点及其对应的IP地址
    """

    try:
        # 读取 dataserv.conf 文件
        conf = configparser.ConfigParser()
        conf.read(conf_url)

        # 获取 [hosts] 部分的列表项
        nodes_ip = conf.items('hosts')
        return nodes_ip

    except:
        print("Error: Failed to load dataserv.conf file")

# 测试函数
# nodes_ip = get_nodes_ip()
# for node, ip in nodes_ip:
#     print(node, ip)
