import threading
import time
import os

def probe_data():
    while True:
        os.system('python data_probe.py')
        time.sleep(3)

def run_physical_model():
    while True:
        os.system('python physical_modeling.py')
        time.sleep(4*60*60) # 4 hours

def calculate_data():
    while True:
        os.system('python calc_data.py')
        time.sleep(2)

def report_data():
    while True:
        os.system('python data_report.py')
        time.sleep(2)

if __name__ == '__main__':
    t1 = threading.Thread(target=probe_data)
    t2 = threading.Thread(target=run_physical_model)
    t3 = threading.Thread(target=calculate_data)
    # t4 = threading.Thread(target=report_data)

    t1.start()
    t2.start()
    t3.start()
    # t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
