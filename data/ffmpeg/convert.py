import csv

# 打开CSV文件并读取数据
with open('55.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# 对数据进行转换和计算
output = []
for row in data:
    x1 = float(row[1])/56
    x2 = float(row[2])
    output_row = [x1, x2, x1**2, x2**2, x1**3, x2**3]
    output.append(output_row)

# 将结果写入CSV文件
with open('ok.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)

