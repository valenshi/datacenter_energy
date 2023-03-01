#!/bin/bash

# 获取所有正在运行的容器的 ID 列表
container_ids=$(docker ps -q)

# 循环处理每个容器
for container_id in $container_ids
do
    # 获取容器名称
    container_name=$(docker inspect --format '{{.Name}}' $container_id)

    # 获取容器使用的 CPU 和内存
    cpu_usage=$(docker stats --no-stream --format "{{.CPUPerc}}" $container_id | tail -n 1 | awk '{gsub(/[^0-9.]/,"",$0); print}')

    mem_usage=$(docker stats --no-stream --format "{{.MemUsage}}" $container_id | tail -n 1 | awk '{print $1}' | awk '{gsub(/[^0-9.]/,"",$0); print}')

    # 输出结果
    echo "$container_name,$cpu_usage,$mem_usage" > data/docker_usage.csv
done
