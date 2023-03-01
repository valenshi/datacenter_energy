#!/bin/bash

# 获取CPU总量
cpu_total=$(grep -c ^processor /proc/cpuinfo)

# 获取所有进程的PID和占用CPU、内存的百分比，并写入process.csv文件
ps -eo pid,%cpu,%mem --sort=-%cpu | awk -v cpu_total="$cpu_total" 'BEGIN { FS=" "; OFS=","; sum_cpu=0; sum_mem=0 } NR>1 { print $1, $2, $3; sum_cpu+=$2; sum_mem+=$3 } END { print "total_usage", sum_cpu, sum_mem }' > data/process_usage.csv
