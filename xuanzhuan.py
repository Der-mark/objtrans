import trimesh
import numpy as np
from trimesh.transformations import rotation_matrix
#####################################################此文件用于旋转一个mesh##################################
# 加载 obj 文件
mesh = trimesh.load('/home/dermark/objtrans/objfile/bear08.obj')

# 创建旋转矩阵，设定旋转角度和轴
angle_in_degrees = -90  # 旋转角度，例如 45 度
angle_in_radians = np.radians(angle_in_degrees)
rotation_axis = [1, 0, 0]  # 例如，围绕 y 轴旋转
rotation_mat = rotation_matrix(angle_in_radians, rotation_axis)

# 应用旋转到 mesh
mesh.apply_transform(rotation_mat)

# 保存旋转后的 mesh 为新的 obj 文件
mesh.export('/home/dermark/objtrans/objfile/bear082.obj')
