import sys
import pandas as pd
import pickle
# 从命令行输入参数中获取需要预测的两个变量
var1 = float(sys.argv[1])
var2 = float(sys.argv[2])
X_predict = [[var1, var2]]

# 加载决策树模型
with open('/root/datacenter_energy/data_collection/ipmi/model.pkl', 'rb') as file:
    dt_model = pickle.load(file)

# 进行预测
y_predict = dt_model.predict(X_predict)

# 输出预测结果
print(y_predict[0])
