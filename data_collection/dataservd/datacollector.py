# -*- coding: UTF-8 -*-
import subprocess
import xmlrpc.client
import threading
import datetime
from time import sleep
import my_tool
# 指定 RPC 服务器的地址和端口号
nodes = my_tool.get_nodes_ip()
vms = my_tool.get_vms()
ipmis = my_tool.get_ipmis()
dc_ipmis = {t[0]:t[1] for t in ipmis}
interval = 1 # 每次采集的间隔时间


# 连接数据库
db = my_tool.MySQLTool(host='node1',username='ecm',password='123456',database='ecm')
result = db.select(table_name='nodedata',columns=['*'])

# 获取时间戳
# 获取当前时间
def getData():
    now = datetime.datetime.now()
    # 将时间转换为时间戳
    timestamp = now.timestamp()
    # 将时间戳转换为指定格式的时间
    time_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_str

def collectHost(ip, hostname):
    try:
        print('collectHost', ip, hostname)
        server_url = "http://" + ip + ":9925/"
        proxy = xmlrpc.client.ServerProxy(server_url)
        result = proxy.hostcollector().split(',')
        if(len(result) < 5):
            return
    except Exception as e:
        print(e)
        return
    
    # 将数据插入到数据库中
    data = {'node_name': result[0], 'timestamp': getData(), 'cpu_load': result[2], 'memory_load':result[3], 'power':result[4]}
    db.insert(table_name='nodedata', data=data)
   
def collectHostCSV(ip, hostname):
    try:
        print('collectHost', ip, hostname)
        power = collectPower(dc_ipmis[hostname])
        server_url = "http://" + ip + ":9925/"
        proxy = xmlrpc.client.ServerProxy(server_url)
        result = proxy.hostcollector()
        if len(result.split(',')) < 2:
            return
    except Exception as e:
        print(e)
        return    
    # 将数据插入到数据库中
    result = result[:-2] + "," + power
    with open("dataset.csv", "a") as f:
        f.write(f"{result}\n")

def collectPod(ip, name):
    try:
        print('collectPod', ip, name)
        server_url = "http://" + ip + ":9925/"
        proxy = xmlrpc.client.ServerProxy(server_url)
        pods = proxy.podcollector().split('\n')
    except Exception as e:
        print(e)
        return
    
    for pod in pods:
        result = pod.split(',')
        if(len(result) < 6):
            continue
        # 将数据插入到数据库中
        data = {'timestamp': getData(),'pod_name': result[1] , 'node_name': result[2],'pod_ip':result[3], 'cpu_load': result[4], 'memory_load':result[5]}
        #print(data)
        db.insert(table_name='poddata', data=data)
   
    return

def collectVM(ip, name):
    try:
        print("collectVM", ip, name)
        # 调用 test.sh 文件并传递名称作为参数
        command = ["../sysstat/vmcollector.sh", name]
        output = subprocess.check_output(command, universal_newlines=True).strip()
        # 获取资源利用率
        server_url = "http://" + ip + ":9925/"
        proxy = xmlrpc.client.ServerProxy(server_url)
        output += ',' + proxy.hostcollector()
        result = output.split(',')
        if(len(result) < 7):
            return
    except Exception as e:
        # 捕获并打印异常，然后继续传播异常
        print("Error occurred while collecting VM data: ", e)
        return

    #插入数据库中
    data = {'vm_name': result[0], 'vm_id': result[1], 'vm_ip': result[2], 'node_name': result[3], 'timestamp': getData(), 'cpu_load': result[-2], 'memory_load': result[-1]}
    db.insert(table_name='vmdata', data=data)

def collectPower(ip):
    command = f"sh ../ipmi/powermon.sh {ip}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode().strip()

def th_collectHost():
    while True:
        sleep(interval)
        for node in nodes:
            # 写入到数据库还是本地csv文件
            # collectHost(node[1], node[0])
            collectHostCSV(node[1],node[0])

def th_collectVM():
    while True:
        sleep(interval)
        for vm in vms:
            collectVM(vm[1], vm[0])
def th_collectPod():
    while True:
        sleep(interval)
        collectPod("192.168.1.202", "node2")

# 创建三个线程，分别循环执行三个函数
thread1 = threading.Thread(target=th_collectHost)
thread2 = threading.Thread(target=th_collectVM)
thread3 = threading.Thread(target=th_collectPod)

# 启动三个线程
thread1.start()
# thread2.start()
# thread3.start()
