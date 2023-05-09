import numpy as np
import sys
import joblib


def predict_lasso(a, b, c):
    # 计算输入特征
    x1, x2, x3, x4, x5, x6 =a, b, c, a**2, b**2, c**2

    # 将特征输入到Numpy数组中
    X_test = np.array([[x1, x2, x3, x4, x5, x6]])

    # 加载预训练好的Lasso模型
    lasso = joblib.load('/root/datacenter_energy/data_processing/modeling/physical/lasso_model.pkl')

    # 预测输出
    y_pred = lasso.predict(X_test)
    return float(y_pred)


args = sys.argv[1:] 
num1 = float(args[0]) 
num2 = float(args[1])
print(predict_lasso(num1,num2,0))
