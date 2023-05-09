#!/usr/bin/env python3

import psutil
import os
import sys

class HiddenPrints:
    def __init__(self, activated=True):
        # activated参数表示当前修饰类是否被激活
        self.activated = activated
        self.original_stdout = None

    def open(self):
        sys.stdout.close()
        sys.stdout = self.original_stdout

    def close(self):
        self.original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        # 这里的os.devnull实际上就是Linux系统中的“/dev/null”
        # /dev/null会使得发送到此目标的所有数据无效化，就像“被删除”一样
        # 这里使用/dev/null对sys.stdout输出流进行重定向

    def __enter__(self):
        if self.activated:
            self.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.activated:
            self.open()




def start_service(service):
    hidden = HiddenPrints()
    
    # 禁用 print
    hidden.close()
    status = status_service(service)
    # 启用 pint
    hidden.open()

    if status:
        print(service + " is already running !")
        return
    
    if service == 'dataprobe':
        os.system('nohup python data_collection/dataservd/dataserv.py >data_collection/logs/dataserv.log 2>&1 & echo $! > .pid')
        print('Data probe service started.')
    elif service == 'collector':
        os.system('nohup python data_collection/dataservd/datacollector.py >data_collection/logs/datacollector.log 2>&1 & echo $! > .pid2')
        print('Data collector service started.')
    else:
        print('Invalid service specified.')

def stop_service(service):
    if service == 'dataprobe':
        if os.path.exists('./.pid'):
            with open('./.pid', 'r') as f:
                pid = f.read().strip()
            os.system(f'kill {pid}')
            os.remove('./.pid')
            print('Data probe service stopped.')
        else:
            print('Data probe service is not running.')
    elif service == 'collector':
        if os.path.exists('./.pid2'):
            with open('./.pid2', 'r') as f:
                pid = f.read().strip()
            os.system(f'kill {pid}')
            os.remove('./.pid2')
            print('Data collector service stopped.')
        else:
            print('Data collector service is not running.')
    else:
        print('Invalid service specified.')

def restart_service(service):
    stop_service(service)
    start_service(service)

# running return True
# not running return False
def status_service(service):
    ret = False
    if service == 'dataprobe':
        if os.path.exists('./.pid'):
            pid_file = open('./.pid', 'r')
            pid = int(pid_file.read())
            pid_file.close()
            process_running = psutil.pid_exists(pid)
            if process_running:
                print('Data probe service is running.\n\n')
                ret = True
            else:
                print('Data probe service is not running.\n\n')
        else:
            print('Data probe service is not running.\n\n')
        os.system("tail -n 10 /root/datacenter_energy/data_collection/logs/dataserv.log")
        print("\n \nFor more information: /root/datacenter_energy/data_collection/logs/ \n")    
    elif service == 'collector':
        if os.path.exists('./.pid2'):
            pid_file = open('./.pid2', 'r')
            pid = int(pid_file.read())
            pid_file.close()
            process_running = psutil.pid_exists(pid)
            if process_running:
                print('Data collector service is running.\n\n')
                ret = True
            else:
                print('Data collector service is not running.\n\n')
        else:
            print('Data collector service is not running.\n\n')
        os.system("tail -n 10 /root/datacenter_energy/data_collection/logs/datacollector.log")
        print("\n \nFor more information: /root/datacenter_energy/data_collection/logs/ \n")
    else:
        print('Invalid service specified.')
    
    return ret

def check_heartbeat():
    os.system('python /root/datacenter_energy/data_collection/dataservd/heartbeat_checker.py')

if __name__ == '__main__':

    # 获取命令参数
    action = sys.argv[1]
    service = sys.argv[2]

    if action == 'start':
        start_service(service)
    elif action == 'stop':
        stop_service(service)
    elif action == 'status':
        status_service(service)
    elif action == 'restart':
        restart_service(service)
    elif action == 'list':
        check_heartbeat()
    else:
        print('Invalid action specified.')
