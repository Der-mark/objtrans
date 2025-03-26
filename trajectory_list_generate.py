import os
#####################################################此文件用于生成trajectory list##################################
# 设置文件夹路径
fn = "/home/dermark/LeapHandGrasp-Der/data/hechengtest1"
fn2="data/hechengtest1"
# 使用 os.listdir 列举文件夹中的所有文件
files = os.listdir(fn)

# 只列出文件名，过滤掉子目录
file_list = [f for f in files if os.path.isfile(os.path.join(fn, f))]

# 打印所有文件名
for file in file_list:
    full_path = os.path.join(fn2, file)  # 拼接完整路径
    print("'"+full_path+"',")