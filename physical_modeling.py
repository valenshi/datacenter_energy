import os
import csv

# 运行model.py文件
os.system("python model.py")

# 清空data/physical_data.csv文件
header = ['cpu%', 'mem%', 'cpu%^2', 'mem%^2', 'cpu%^3', 'mem%^3', 'power']
with open("data/physical_data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)

