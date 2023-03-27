import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# 读取数据集
data = pd.read_csv('dataset.csv')
X = data.iloc[:, :2]  # 特征为前两列
y = data.iloc[:, 2]  # 目标值为第三列

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 定义决策树模型
dt_reg = DecisionTreeRegressor(random_state=0)

# 训练模型
dt_reg.fit(X_train, y_train)

# 预测测试集结果
y_pred = dt_reg.predict(X_test)

# 评估模型，使用R2分数
r2 = r2_score(y_test, y_pred)
print("R2 score: {:.2f}".format(r2))

