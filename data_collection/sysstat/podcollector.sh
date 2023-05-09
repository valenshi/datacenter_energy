#!/bin/bash

# 获取所有 Pod 的名称和所在主机名
pod_info=$(kubectl get pods -o=custom-columns=POD:.metadata.name,NODE:.spec.nodeName --no-headers)

# 获取主机的 CPU 和内存利用率
node_info=$(kubectl top node --no-headers)

# 输出表头
# echo "Pod  CPU%  Pod Mem%  Node CPU%  Node Mem%  Pod Name   Node Name"


# 对每个Pod进行循环
while read -r pod_name node_name; do
  pod_status=$(kubectl get pod "$pod_name" -o=jsonpath='{.status.phase}')
  if [ "$pod_status" != "Running" ]; then
    echo "$pod_name 跳过: Pod 状态为 $pod_status"
    continue
  fi
  # 获取该Pod的CPU和内存利用率
  timestamp=$(date +"%Y-%m-%d %H:%M:%S") 

  pod_metrics=$(kubectl top pods "$pod_name" --no-headers -n $(kubectl get pod "$pod_name" -o=jsonpath='{.metadata.namespace}'))
  # echo "$pod_metrics"
  # 从输出中提取 CPU 和内存利用率
  
  pod_cpu=$(echo "$pod_metrics" | awk '{print $2}' | tr -d '%' | grep -o "[0-9.]*")
  pod_mem=$(echo "$pod_metrics" | awk '{print $3}' | tr -d '%' | grep -o "[0-9.]*")
  #echo "cpu, mem: $pod_cpu, $pod_mem"
  # 获取其所在节点的CPU和内存利用率
  node_metrics=$(echo "$node_info" | grep "$node_name")
  node_cpu=$(echo "$node_metrics" | awk '{print $2}' | tr -d '%' | tr -d '%' | grep -o "[0-9.]*")
  node_mem=$(echo "$node_metrics" | awk '{print $3}' | tr -d '%' | tr -d '%' | grep -o "[0-9.]*")
  #echo "node_cpu, node_mem: $node_cpu, $node_mem"
  # 计算Pod和节点的CPU和内存使用率比率
  cpu_ratio=$(echo "scale=2; $pod_cpu / $node_cpu" | bc)
  mem_ratio=$(echo "scale=2; $pod_mem / $node_mem" | bc)

  pod_ip=$(kubectl get pod $pod_name -o jsonpath='{.status.podIP}')
  # 输出结果
  
  echo "$timestamp,$pod_name,$pod_ip,$node_name,$cpu_ratio,$mem_ratio"
 # printf "%6s%%  %6s%%  %7s%%  %7s%%   %-20s %s\n" "$pod_cpu" "$pod_mem" "$node_cpu" "$node_mem" "$pod_name" "$node_name"

done <<< "$pod_info"
