#!/bin/bash

# 创建文件头
# echo "timestamp,cpu%,mem%,cpu%^2,mem%^2,cpu%^3,mem%^3" > data.csv

# 获取时间戳，并将其转换成YYYY-mm-dd HH:MM:SS格式
timestamp=$(date +"%H:%M:%S")

# 获取CPU总负载
cpu_load=$(top -bn1 | awk 'NR>7{s+=$9/23} END {print s}')

# 获取内存使用百分比
mem_usage=$(free | awk '/Mem/{printf "%.2f", $3/$2 * 100.0}')

# 计算CPU百分比的平方和三次方
cpu_square=$(echo "$cpu_load^2" | bc)
cpu_cube=$(echo "$cpu_load^3" | bc)

# 计算内存百分比的平方和三次方
mem_square=$(echo "$mem_usage^2" | bc)
mem_cube=$(echo "$mem_usage^3" | bc)

# 将数据写入文件
echo ",$timestamp,$cpu_load,$mem_usage,$cpu_square,$mem_square,$cpu_cube,$mem_cube" >> data/physical_data.csv
echo "$timestamp,$cpu_load,$mem_usage,$cpu_square,$mem_square,$cpu_cube,$mem_cube" >> data/physical_now_usage.csv
