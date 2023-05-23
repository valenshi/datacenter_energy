import pandas as pd

# 读取原始数据集
dataset = pd.read_csv('dataset.csv')

# 过滤compute1列和倒数第二列大于0.1的数据
mask = (dataset.iloc[:, 0] == 'comput2') & (dataset.iloc[:, -3] > 1.1 )  & (dataset.iloc[:, -3] < 100.0)
compute1_data = dataset.loc[mask]

# 存储到新文件
compute1_data.to_csv('dataset1.csv', index=False)