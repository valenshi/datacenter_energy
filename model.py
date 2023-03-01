import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score, mean_squared_error
import pickle

# 读取训练数据和测试数据
train_data = pd.read_csv('data/physical_data.csv')

# 从训练数据中提取输入特征和输出标签
X_train = train_data.iloc[:, :-1].values
y_train = train_data.iloc[:, -1].values

# 创建Lasso回归模型
lasso = Lasso(alpha=0.1, max_iter=10000)

# 拟合训练数据
lasso.fit(X_train, y_train)

# 保存模型为文件
with open('data/lasso_model.pkl', 'wb') as file:
    pickle.dump(lasso, file)

# 获得每个特征的系数
feature_names = train_data.columns[:-1]
coefficients = lasso.coef_

# 输出每个特征的系数到文件
with open('data/coef.out', 'w') as file:
    file.write('{}: {}\n'.format('intercept_', lasso.intercept_))
    for feature, coef in zip(feature_names, coefficients):
        file.write('{}: {}\n'.format(feature, coef))
