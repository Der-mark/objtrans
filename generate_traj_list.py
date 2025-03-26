import os
#############################本文件用于将reference traj分类打包到几个独立文件夹path中###################
import os
import shutil

# 设置你的文件夹路径
folder_path = "/home/dermark/GRAB/grab_save4/"  # 请根据实际情况修改

# 获取该文件夹下所有npy文件的文件名
npy_files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]

# 筛选出包含 'lift', 'inspect', 'pass_' 词条的文件
lift_files = [f for f in npy_files if 'lift' in f]
inspect_files = [f for f in npy_files if 'inspect' in f]
pass_files = [f for f in npy_files if 'pass_' in f]

# 创建文件夹，如果文件夹不存在，则创建
output_folders = ['lift', 'inspect', 'pass_', 'other']
for folder in output_folders:
    output_path = os.path.join(folder_path, folder)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

# 将文件分类并复制到相应文件夹
def copy_files(file_list, folder_name):
    for file in file_list:
        src = os.path.join(folder_path, file)
        dest = os.path.join(folder_path, folder_name, file)
        shutil.copy(src, dest)

# 复制文件到对应的文件夹
copy_files(lift_files, 'lift')
copy_files(inspect_files, 'inspect')
copy_files(pass_files, 'pass_')

# 复制不包含指定词条的文件到 'other' 文件夹
other_files = [f for f in npy_files if 'lift' not in f and 'inspect' not in f and 'pass_' not in f]
copy_files(other_files, 'other')

print("文件已成功分类并复制到相应文件夹。")
