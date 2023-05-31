import sys
import pandas as pd
import pickle
path = "/root/datacenter_energy/data_processing/modeling/physical/"
# 从命令行输入参数中获取需要预测的两个变量
var1 = float(sys.argv[1])
var2 = float(sys.argv[2])

# 输出预测结果

def predict(cpu_load, mem_load):
    # 加载决策树模型
    X_predict = [[cpu_load, mem_load]]
    with open(path+'decision_tree_model.pkl', 'rb') as file:
        dt_model = pickle.load(file)

    # 进行预测
    y_predict = dt_model.predict(X_predict)
    return y_predict[0]

print(predict(var1, var2))