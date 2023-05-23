import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
import pickle

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler

from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV


def make_dataset(file_path):
    # 读取数据集
    dataset = pd.read_csv(file_path)

    # 提取输入特征和输出标签
    X = dataset.iloc[:, -3:-1].values
    y = dataset.iloc[:, -1].values

    # 划分训练集和测试集
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=1)

    return X_train, y_train, X_test, y_test


def build_mlp_model(X_train, y_train, X_test, y_test):
    print("build_mlp_model")
    # 对输入特征进行标准化处理
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 创建神经网络回归模型
    mlp = MLPRegressor(hidden_layer_sizes=(10,), max_iter=10000, random_state=1)
    # 拟合训练数据
    mlp.fit(X_train_scaled, y_train)
    y_pred = mlp.predict(X_test_scaled)

    # 输出误差信息
    len_ = len(y_pred)
    cnt = 0
    mi = 11
    mx = 0
    for i in range(len_):
        err = (y_pred[i]-y_test[i])/y_test[i]
        if(abs(err) > 0.1):
            cnt += 1
        # print(y_pred[i], y_test[i], err)
        mx = max(err,mx)
        mi = min(mi, err)

    print("总计：", len_, cnt, mx, mi)

    # 输出模型评估指标
    print("rate:               ",cnt/len_)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print("R2 Score:           ", r2)
    print("Mean Squared Error: ", mse)

    # # 保存模型为文件
    # with open('mlp_model.pkl', 'wb') as file:
    #     pickle.dump(mlp, file)

    # # 获取每个特征的系数
    # coefs = mlp.coefs_

    # # 输出每个特征的系数到文件
    # print("intercepts_: ", mlp.intercepts_)
    # for coef in coefs:
    #     file.write('\n')
    #     for c in coef:
    #         file.write('{}\n'.format( c))
    # file.close()

def build_decision_tree_model(X_train, y_train, X_test, y_test, max_depth=5):
    print("build_decision_tree_model")
    # 创建决策树回归模型
    dt = DecisionTreeRegressor(random_state=1, max_depth=max_depth)
    # 拟合训练数据
    dt.fit(X_train, y_train)
    y_pred = dt.predict(X_test)

    # 输出误差信息
    # len_ = len(y_pred)
    # cnt = 0
    # mi = 11
    # mx = 0
    # for i in range(len_):
    #     err = (y_pred[i]-y_test[i])/y_test[i]
    #     if(abs(err) > 0.1):
    #         cnt += 1
    #     # print(y_pred[i], y_test[i], err)
    #     mx = max(err,mx)
    #     mi = min(mi, err)

    # print("总计：", len_, cnt, mx, mi)

    # 输出模型评估指标
    # print("rate:               ",cnt/len_)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print("R2 Score:           ", r2)
    print("Mean Squared Error: ", mse)

    # 保存模型为文件
    with open('decision_tree_model.pkl', 'wb') as file:
        pickle.dump(dt, file)

    # 获取每个特征的重要性
    # importances = dt.feature_importances_

    # # 输出每个特征的重要性到文件
    # print("feature_importances: ", importances)

    # with open('importances.out', 'w') as file:
    #     for importance in importances:
    #         file.write('{}\n'.format( importance))
    # file.close()



def build_svm_model(X_train, y_train, X_test, y_test, kernel='rbf'):
    print("build_svm_model")
    # 对输入特征进行标准化处理
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 创建支持向量机回归模型
    svr = SVR(kernel=kernel, C=100, gamma=0.1, epsilon=.1)
    # 拟合训练数据
    svr.fit(X_train_scaled, y_train)
    y_pred = svr.predict(X_test_scaled)

    # 输出误差信息
    len_ = len(y_pred)
    cnt = 0
    mi = 11
    mx = 0
    for i in range(len_):
        err = (y_pred[i]-y_test[i])/y_test[i]
        if(abs(err) > 0.1):
            cnt += 1
        # print(y_pred[i], y_test[i], err)
        mx = max(err,mx)
        mi = min(mi, err)

    print("总计：", len_, cnt, mx, mi)

    # 输出模型评估指标
    print("rate:               ",cnt/len_)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print("R2 Score:           ", r2)
    print("Mean Squared Error: ", mse)

    # # 保存模型为文件
    # with open('svm_model.pkl', 'wb') as file:
    #     pickle.dump(svr, file)

    # # 获取每个特征的支持向量数目和权重
    # support = svr.support_
    # support_vectors = svr.support_vectors_
    # dual_coef = svr.dual_coef_

    # # 输出每个特征的支持向量数目和权重到文件
    # print("Number of support vectors: ", support.shape[0])
    # for i in range(support.shape[0]):
    #     index = support[i]
    #     coef = dual_coef[0][i]
    #     vector = support_vectors[i]
    #     file.write('index: {}, coef: {}, vector: {}\n'.format(index, coef, vector))
    # file.close()

def build_random_forest_model(X_train, y_train, X_test, y_test):
    print("build_random_forest_model")
    # 创建随机森林回归模型
    rf = RandomForestRegressor(n_estimators=100, random_state=1)
    # 拟合训练数据
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    # 输出误差信息
    len_ = len(y_pred)
    cnt = 0
    mi = 11
    mx = 0
    for i in range(len_):
        err = (y_pred[i]-y_test[i])/y_test[i]
        if(abs(err) > 0.1):
            cnt += 1
        # print(y_pred[i], y_test[i], err)
        mx = max(err,mx)
        mi = min(mi, err)

    print("总计：", len_, cnt, mx, mi)

    # 输出模型评估指标
    print("rate:               ",cnt/len_)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print("R2 Score:           ", r2)
    print("Mean Squared Error: ", mse)

    # # 保存模型为文件
    # with open('random_forest_model.pkl', 'wb') as file:
    #     pickle.dump(rf, file)

    # # 获取每个特征的重要性
    # importances = rf.feature_importances_

    # # 输出每个特征的重要性到文件
    # print("feature_importances: ", importances)

    # with open('importances.out', 'w') as file:
    #     for importance in importances:
    #         file.write('{}\n'.format( importance))


def build_model(X_train, y_train, X_test, y_test, alpha=0.05, degree=2):
    print("build_lasso")
    # 将输入特征拓展为多项式特征
    poly = PolynomialFeatures(degree=degree)
    X_train = poly.fit_transform(X_train)
    X_test = poly.transform(X_test)

    # 创建Lasso回归模型
    lasso = Lasso(alpha=alpha, max_iter=1000000000)
    # 拟合训练数据
    lasso.fit(X_train, y_train)
    y_pred = lasso.predict(X_test)

    # 输出误差信息
    len_ = len(y_pred)
    cnt = 0
    mi = 11
    mx = 0
    for i in range(len_):
        err = (y_pred[i]-y_test[i])/y_test[i]
        if(abs(err) > 0.1):
            cnt += 1
        # print(y_pred[i], y_test[i], err)
        mx = max(err,mx)
        mi = min(mi, err)

    print("总计：", len_, cnt, mx, mi)

    # 输出模型评估指标
    print("rate:               ",cnt/len_)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print("R2 Score:           ", r2)
    print("Mean Squared Error: ", mse)

    # # 保存模型为文件
    # with open('lasso_model.pkl', 'wb') as file:
    #     pickle.dump(lasso, file)

    # # 获取每个特征的系数
    # coefficients = lasso.coef_

    # # 输出每个特征的系数到文件
    # print("lasso.intercept_:   ",lasso.intercept_)
    # print("coef: ", coefficients)

    # with open('coef.out', 'w') as file:
    #     file.write('{}: {}\n'.format('intercept_', lasso.intercept_))
    #     for coef in coefficients:
    #         file.write('{}\n'.format( coef))

# 使用例子
X_train, y_train, X_test, y_test = make_dataset('dataset1.csv')
# build_model(X_train, y_train, X_test, y_test, alpha=0.05,degree=2)
# build_svm_model(X_train, y_train, X_test, y_test)
# build_random_forest_model(X_train, y_train, X_test, y_test)
# build_mlp_model(X_train, y_train, X_test, y_test)
build_decision_tree_model(X_train, y_train, X_test, y_test)
