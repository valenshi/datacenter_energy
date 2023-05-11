#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <IPMI IP address>"
  exit 1
fi

ipmi_ip=$1
output=$(ipmitool -H $ipmi_ip -I lanplus -U admin -P admin sdr elist | grep Total_Power)
last_power=$(echo $output | awk '{print $(NF-1)}')
echo $last_power
