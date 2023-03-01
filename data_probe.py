import subprocess
import time

# 执行get_power.sh脚本
cmd_get_power = 'bash get_power.sh'
process_get_power = subprocess.Popen(cmd_get_power.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output_get_power, error_get_power = process_get_power.communicate()

# 将输出保存到日志文件中
with open('logs/get_power.log', 'a') as f:
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    f.write(f'[{timestamp}] Output of {cmd_get_power}:\n')
    f.write(output_get_power.decode())
    f.write(error_get_power.decode())
    f.write('\n')

# 执行physical_usage.sh脚本
cmd_physical_usage = 'bash physical_usage.sh'
process_physical_usage = subprocess.Popen(cmd_physical_usage.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output_physical_usage, error_physical_usage = process_physical_usage.communicate()

# 将输出保存到日志文件中
with open('logs/get_power.log', 'a') as f:
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    f.write(f'[{timestamp}] Output of {cmd_physical_usage}:\n')
    f.write(output_physical_usage.decode())
    f.write(error_physical_usage.decode())
    f.write('\n')

