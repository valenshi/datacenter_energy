#!/bin/bash

# 检查是否提供了虚拟机名称
if [ -z "$1" ]; then
    echo "请提供虚拟机名称"
    exit 1
else
    vm_name=$1
fi

# 获取虚拟机的ID和其他信息
vm_info=$(openstack server show $vm_name -f json)

# 检查是否找到了虚拟机
if [ -z "$vm_info" ]; then
    echo "找不到名为$vm_name的虚拟机"
    exit 1
fi

# 从服务器信息中提取虚拟机的ID、IP地址和所在节点的名称，并打印到终端
vm_id=$(echo "$vm_info" | jq -r '.id')
node_name=$(echo "$vm_info" | jq -r '.["OS-EXT-SRV-ATTR:host"]')
vm_ips=$(echo "$vm_info" | jq -r '.addresses' | sed 's/,/ /g')

# 打印虚拟机的名称、ID、IP地址和所在节点
for vm_ip in $vm_ips; do
    echo "${vm_name},${vm_id},${vm_ip},${node_name}"
done
