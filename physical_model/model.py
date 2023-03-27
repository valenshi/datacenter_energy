#encoding: utf-8
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score, mean_squared_error
import pickle
path = "/Users/valenshi/codeRepository/ECM/"
# 读取训练数据和测试数据
train_data = pd.read_csv(path+'data/physical_data.csv')
test_data = pd.read_csv(path+'data/physical_proving.csv')

# 从训练数据中提取输入特征和输出标签
X_train = train_data.iloc[1:,1:].values
y_train = train_data.iloc[1:,0 ].values

# 从测试数据中提取输入特征和输出标签
X_test = test_data.iloc[:, 1:].values
y_test = test_data.iloc[:, 0].values

# 创建Lasso回归模型
lasso = Lasso(alpha=0.05, max_iter=1000000)

# 拟合训练数据
lasso.fit(X_train, y_train)
y_pred = lasso.predict(X_test)
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
    # dataSet.append([float(y_pred[i]),float(y_test[i]), err])
    mx = max(err,mx)
    mi = min(mi, err)
    

print("总计：", len_, cnt, mx, mi)

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("R2 Score: ", r2)
print("Mean Squared Error: ", mse)

# 保存模型为文件
with open(path+'data/lasso_model.pkl', 'wb') as file:
    pickle.dump(lasso, file)

# 获得每个特征的系数
feature_names = train_data.columns[:-1]
coefficients = lasso.coef_

# 输出每个特征的系数到文件
print("lasso.intercept_: ",lasso.intercept_)
print("coef: ", coefficients)

with open(path+'data/coef.out', 'w') as file:
    file.write('{}: {}\n'.format('intercept_', lasso.intercept_))
    for feature, coef in zip(feature_names, coefficients):
        file.write('{}: {}\n'.format(feature, coef))
