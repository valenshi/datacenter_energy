#encoding: utf-8
#encoding: utf-8
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge, ElasticNet, BayesianRidge, HuberRegressor, PassiveAggressiveRegressor, OrthogonalMatchingPursuit, TheilSenRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
import random
import csv


def writeResult(a,b):
    with open('predict.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a, b])

path = "/Users/valenshi/codeRepository/ECM/"
# 读取训练数据和测试数据
data = pd.read_csv('dataset.csv')

# 将数据集随机分为训练集和测试集
train_size = int(len(data) * 0.6)
indices = list(range(len(data)))
random.shuffle(indices)
train_indices = indices[:train_size]
test_indices = indices[train_size:]

train_data = data.iloc[train_indices]
test_data = data.iloc[test_indices]

# 从训练数据中提取输入特征和输出标签
X_train = train_data.iloc[:,:-1].values
y_train = train_data.iloc[:,-1].values/3600000

# 从测试数据中提取输入特征和输出标签
X_test = test_data.iloc[:, :-1].values
y_test = test_data.iloc[:, -1].values/3600000



poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.fit_transform(X_test)


huber_regressor = HuberRegressor()
huber_regressor.fit(X_train_poly, y_train)
y_pred = huber_regressor.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Huber Regressor:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()

len_ = len(y_pred)
cnt = 0
mi = 11
mx = 0
# fp = open("pred_data.csv","w")
# dataSet = []
for i in range(len_):
    err = (y_pred[i]-y_test[i])/y_test[i]
    if(abs(err) > 0.1):
        cnt += 1
    print(y_pred[i], y_test[i], err)
    writeResult(y_test[i],y_pred[i])
    # dataSet.append([float(y_pred[i]),float(y_test[i]), err])
    mx = max(err,mx)
    mi = min(mi, err)
    

print("总计：", len_, cnt, mx, mi)
