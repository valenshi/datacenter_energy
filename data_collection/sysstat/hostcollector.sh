#!/bin/bash
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
# 获取当前时刻的 CPU 使用百分比
cpu_usage=$(mpstat 1 1 | grep -e "平均时间" -e "Average" | awk '$12 ~ /[0-9.]+/ { print 100 - $12 }')

# 获取当前时刻的内存使用百分比
mem_usage=$(free | awk '/^Mem/ { print $3/$2 * 100.0 }')
result=$(python /root/datacenter_energy/data_collection/ipmi/predict.py $cpu_usage $mem_usage)

# 输出结果
echo "$(hostname),$timestamp,$cpu_usage,$mem_usage,$result"
