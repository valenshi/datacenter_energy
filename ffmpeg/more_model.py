#encoding: utf-8
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge, ElasticNet, BayesianRidge, HuberRegressor, PassiveAggressiveRegressor, OrthogonalMatchingPursuit, TheilSenRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
import random
import csv


path = "/Users/valenshi/codeRepository/ECM/"
# 读取数据
data = pd.read_csv('dataset.csv')

# 将数据集随机分为训练集和测试集
train_size = int(len(data) * 0.8)
indices = list(range(len(data)))
random.shuffle(indices)
train_indices = indices[:train_size]
test_indices = indices[train_size:]

train_data = data.iloc[train_indices]
test_data = data.iloc[test_indices]

# 从训练数据中提取输入特征和输出标签
X_train = train_data.iloc[:,:-1].values
y_train = train_data.iloc[:,-1].values

# 从测试数据中提取输入特征和输出标签
X_test = test_data.iloc[:, :-1].values
y_test = test_data.iloc[:, -1].values



def writeResult(model_name,r2,mse):
    with open('result.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([model_name, r2, mse])

# 多项式拟合
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.fit_transform(X_test)

print("----- 多项式拟合 -----")
# Linear Regression
lr = LinearRegression()
lr.fit(X_train_poly, y_train)
y_pred = lr.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("Linear Regression:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("Linear Regression",r2,mse)

# Lasso
lasso = Lasso(alpha=0.05, max_iter=1000000)
lasso.fit(X_train_poly, y_train)
y_pred = lasso.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Lasso Regression:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("Lasso Regression",r2,mse)

# Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_poly, y_train)
y_pred = ridge.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Ridge Regression:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("Ridge Regression",r2,mse)


#ElasticNet
elastic_net = ElasticNet(alpha=0.05, l1_ratio=0.5, max_iter=1000000)
elastic_net.fit(X_train_poly, y_train)
y_pred = elastic_net.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("ElasticNet Regression:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("ElasticNet Regression",r2,mse)

# BayesianRidge

bayesian_ridge = BayesianRidge()
bayesian_ridge.fit(X_train_poly, y_train)
y_pred = bayesian_ridge.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Bayesian Ridge Regression:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("Bayesian Ridge Regression",r2,mse)

# HuberRegressor

huber_regressor = HuberRegressor()
huber_regressor.fit(X_train_poly, y_train)
y_pred = huber_regressor.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Huber Regressor:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("Huber Regressor",r2,mse)

# OrthogonalMatchingPursuit
omp = OrthogonalMatchingPursuit()
omp.fit(X_train_poly, y_train)
y_pred = omp.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Orthogonal Matching Pursuit:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("Orthogonal Matching Pursuit",r2,mse)

# TheilSenRegressor
theil_sen_regressor = TheilSenRegressor()
theil_sen_regressor.fit(X_train_poly, y_train)
y_pred = theil_sen_regressor.predict(X_test_poly)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Theil-Sen Regressor:")
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)
print()
writeResult("Theil-Sen Regressor",r2,mse)




