# -*- coding: UTF-8 -*-
import sys
import os
import time

# 将 utils 目录添加到路径中
sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils/database'))
# 导入 my_tool 模块
from getnodeip import get_nodes_ip,get_host_ip,get_vms,get_ipmis

from mysqltool import MySQLTool




# test
#if __name__ == '__main__':
    # 实例化 MySQL 工具类
#    db_tool = MySQLTool(host='10.168.1.201', username='ecm', password='123456', database='ecm')

    # 每隔 10 秒钟查询一次数据库
#    while True:
#        result = db_tool.select(table_name='nodedata', columns=['id', 'node_name'])
#        print(result)
#        time.sleep(10)
