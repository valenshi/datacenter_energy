import pandas as pd
import csv
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import sys

# 加载训练好的模型
lasso = joblib.load('data/lasso_model.pkl')

# 读取输入数据
data = pd.read_csv('data/physical_now_usage.csv', usecols=[1,2,3,4,5,6])
x1, x2, x3, x4, x5, x6 = data.values.tolist()[0]



# 构造输入特征
X_test = np.array([[x1, x2, x3, x4, x5, x6]])

# 对输入特征进行多项式扩展

# 进行预测
y_pred = lasso.predict(X_test)

# 读取coef.out文件，获取系数
with open('data/coef.out', 'r') as file:
    lines = file.readlines()
    coef = [float(line.split()[1]) for line in lines]

# 获取Y_test
Y_test = coef[:]

# 计算p1
cpu_power = X_test[0][0]*Y_test[1] + X_test[0][2]*Y_test[3] + X_test[0][4]*Y_test[5]


# 计算p2
mem_power =  X_test[0][1]*Y_test[2] + X_test[0][3]*Y_test[4] + X_test[0][5]*Y_test[6]

# 输出预测结果
result = str(y_pred[0])

# 将结果写入到csv文件中
with open('data/physical_predict.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow([result, cpu_power,mem_power,Y_test[0]])