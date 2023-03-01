#encoding: utf-8
import csv
import subprocess

# 执行get_docker_usage.sh和get_job_usage.sh脚本
subprocess.run(["bash", "get_docker_usage.sh"])
subprocess.run(["bash", "get_job_usage.sh"])

# 从process_usage.csv中读取数据
process_usage = []
with open("data/process_usage.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] == "total_usage":
            all_usage = [float(row[1]), float(row[2])]
            break
        process_usage.append([float(row[1]), float(row[2])])

# 从docker_usage.csv中读取数据
docker_usage = []
with open("data/docker_usage.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        docker_usage.append([float(row[1]), float(row[2])])

# 从physical_predict.csv中读取数据
with open("data/physical_predict.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    row = next(reader)
    physical_predict = [float(row[1]), float(row[2]), float(row[3])]

# 计算process_frac
process_frac = []
for row in process_usage:
    process_frac.append([(row[0]/all_usage[0])*physical_predict[0] + (row[1]/all_usage[1])*physical_predict[1]])

# 计算docker_frac
docker_frac = []
for row in docker_usage:
    docker_frac.append([(row[0]/all_usage[0])*physical_predict[0] + (row[1]/all_usage[1])*physical_predict[1]])

# 计算process_predict
process_predict = []
for row in process_frac:
    process_predict.append(row[0])

# 计算docker_predict
docker_predict = []
for row in docker_frac:
    docker_predict.append(row[0])
process_predict = sorted(process_predict)
docker_predict = sorted(docker_predict)
# 输出结果
print("Process Prediction:")
print(process_predict)
print("Docker Prediction:")
print(docker_predict)