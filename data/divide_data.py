import csv
import random

# 打开 rawdata.csv 文件
with open('rawdata.csv', newline='') as f:
    reader = csv.reader(f)
    # 将文件内容存储为列表
    data = [row for row in reader]

# 随机打乱数据
random.shuffle(data)

# 计算分割点
split_point = int(len(data) * 0.75)

# 将数据分为训练集和验证集
train_data = data[:split_point]
proving_data = data[split_point:]

# 将训练集写入 physical_data.csv 文件
with open('physical_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(train_data)

# 将验证集写入 physical_proving.csv 文件
with open('physical_proving.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(proving_data)

