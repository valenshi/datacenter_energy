import pandas as pd
import pickle
import csv
import os

path = "/Users/valenshi/codeRepository/ECM/"
model_path = os.path.join(path, "data/lasso_model.pkl")
csv_path_template = os.path.join(path, "data/mnist/{}.csv")
output_path_template = os.path.join(path, "data/mnist/{}_output.csv")

# 预处理数据
output_data = []
for i in range(1, 28):
    # 打开CSV文件并读取数据
    with open(csv_path_template.format(i), 'r', newline='') as file:
        reader = csv.reader(file)
        # next(reader)  # 忽略掉第一行（表头）
        data = list(reader)

    # 对数据进行转换和计算
    output = []
    for row in data:
        x1 = float(row[1])/56
        x2 = float(row[2])
        output_row = [x1, x2, x1**2, x2**2, x1**3, x2**3]
        output.append(output_row)

    # 将结果加入输出数据列表
    output_data.append(output)

# 从pkl文件中读取Lasso模型
with open(model_path, 'rb') as f:
    lasso_model = pickle.load(f)

ans_list = []

for i in range(1, 28):
    # 将输出数据写入CSV文件
    with open(output_path_template.format(i), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output_data[i-1])

    # 读取输出文件并进行预测
    sum = 0
    with open(output_path_template.format(i), 'r') as f:
        for line in f:
            # 将每一行数据分割成6个值，并将它们转换为float类型
            data = list(map(float, line.strip().split(',')[0:6]))
            # 转换数据成Pandas Series对象
            data = pd.Series(data, index=['x1', 'x2', 'x1^2', 'x2^2', 'x1^3', 'x2^3'])
            # 使用模型进行预测
            prediction = lasso_model.predict([data])
            # 将预测结果加入结果列表
            sum = sum+float(prediction[0]-35.638)*4
    print(i,".csv sum is :", sum)


