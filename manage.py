#!/usr/bin/env python3

import psutil
import os
import sys

def start_service(service):
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

def status_service(service):
    if service == 'dataprobe':
        if os.path.exists('./.pid'):
            pid_file = open('./.pid', 'r')
            pid = int(pid_file.read())
            pid_file.close()
            process_running = psutil.pid_exists(pid)
            if process_running:
                print('Data probe service is running.\n\n')
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
            else:
                print('Data collector service is not running.\n\n')
        else:
            print('Data collector service is not running.\n\n')
        os.system("tail -n 10 /root/datacenter_energy/data_collection/logs/datacollector.log")
        print("\n \nFor more information: /root/datacenter_energy/data_collection/logs/ \n")
    else:
        print('Invalid service specified.')

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
