#!/bin/bash

# 执行命令并将结果输出到文件末尾
echo -n "$(ipmitool -H 11.11.12.1 -I lanplus -U admin -P admin sdr elist | grep "Total_Power" | awk '{print $(NF-1)}')" >> data/physical_data.csv

