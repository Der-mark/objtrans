import os
import re
#############################本文件用于生成objectname的urdf序列#################
# 设置文件夹路径
folder_path = "/home/dermark/GRAB/grab_save4/"  # 请修改为你实际的文件夹路径

# 获取该文件夹下所有npy文件的文件名
npy_files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]

# 定义一个函数来提取物体名
def extract_object_name(filename):
    # 使用正则表达式提取文件名中"s1"或"s2"之后的物体名称
    match = re.search(r"(s[12]_[a-zA-Z0-9]+)", filename)
    if match:
        return match.group(1).split('_')[1]  # 提取出物体名部分
    return None

# 遍历npy文件并提取物体名
for file in npy_files:
    object_name = extract_object_name(file)
    if object_name:
        # 在此修改文件名或对象文件名
        # 这里我们假设你需要替换成与物体相关的 URDF 文件名
        new_object_name = f"urdf/objects/GRAB/{object_name}/{object_name}.urdf"
        print(f"Original File: {file}, New Object File: {new_object_name}")
