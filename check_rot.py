import os
import numpy as np
#############################本文件用于检测哪些reference trajectory没有linkrot，并把它们删掉###################
# 设置文件夹路径
folder_path = "/home/dermark/GRAB/grab_save4/"  # 请修改为实际的文件夹路径

# 获取该文件夹下所有npy文件的文件名
npy_files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]

# 定义一个函数来检查npy文件的key并删除缺少键的文件
def check_and_delete_npy_files(npy_files, folder_path):
    for file in npy_files:
        file_path = os.path.join(folder_path, file)
        try:
            # 加载npy文件
            data = np.load(file_path, allow_pickle=True).item()
            # 检查'link_key_to_link_rot'是否存在
            if 'link_key_to_link_rot' not in data:
                print(f"File missing 'link_key_to_link_rot': {file}, deleting it...")
                # 删除文件
                os.remove(file_path)
        except Exception as e:
            print(f"Error loading {file}: {e}")

# 调用函数检查并删除缺少'link_key_to_link_rot'的npy文件
check_and_delete_npy_files(npy_files, folder_path)
