import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.rc("font",family='PingFang HK')
# 读取数据文件
data = pd.read_csv('predict.csv')

# 设置X轴数据为行号
x = data.index.tolist()

# 设置Y轴数据为第一列和第二列
y1 = data.iloc[:, 0].tolist()
y2 = data.iloc[:, 1].tolist()

# 绘制并列柱状图
fig, ax = plt.subplots()
# width = 0.3
ax.bar(x, y1, width=0.4, align='edge', color='#87CEFA',label='Predicted Energy Comsumption')
ax.bar(x, y2, width=-0.4, align='edge',color='#DA70D6',  label='Actual Energy Comsumption')
# ax.bar(x - width/2, y1, width=width, color='#87CEEB', label='Y1')

# # 绘制Y2轴柱状图
# ax.bar(x + width/2, y2, width=width, color='#9370DB', label='Y2')
# 设置图例
ax.legend()

# 设置X轴标签和标题
ax.set_xlabel('Sampling sequence number')
ax.set_ylabel('Energy Consumption(kwh)')
# ax.set_title('Measured and predicted power consumption of containers')

# 显示图形
# plt.show()

plt.savefig('fg4-2.eps', format='eps', dpi=1600, bbox_inches='tight')
