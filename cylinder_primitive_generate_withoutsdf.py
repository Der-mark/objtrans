import numpy as np
import random
import trimesh
from mesh_to_sdf import mesh_to_sdf
import pyrender
#############################本文件用于给物体生成cylinderlike的object primitive###################
# 加载目标网格对象
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/flashlight/flashlight.obj')

# 生成随机查询点（用于计算 SDF）
query_points = np.random.uniform(-0.2, 0.2, size=(125000, 3))

# 使用 mesh_to_sdf 获取目标网格的 SDF
sdf_object = mesh_to_sdf(object_mesh, query_points)

# 初始解和温度
r, h, t1, t2, t3 = 0.02, 0.05, 0.01 * random.uniform(-1, 1), 0.01 * random.uniform(-1, 1), 0.01 * random.uniform(-1, 1)
T = 10000
T_min = 1e-3
alpha = 0.99
current_value = 0

# 计算圆柱的 SDF（使用闭式解）
def cylinder_sdf(points, radius, height, center):
    """计算圆柱体的 SDF"""
    # 计算点到圆柱轴线的距离（即xy平面上的投影距离）
    xy_dist = np.linalg.norm(points[:, :2] - center[:2], axis=1) - radius
    
    # 计算点在z轴上的距离
    z_dist = np.abs(points[:, 2] - center[2]) - height / 2

    # 对于xy距离和z距离，取较大的一个作为 SDF
    sdf = np.maximum(xy_dist, z_dist)
    
    return sdf

# 目标函数：基于 SDF 计算 IoU
def objective(r, h, t1, t2, t3):
    # 计算圆柱的 SDF
    cylinder_center = np.array([t1, t2, t3])
    sdf_cylinder = cylinder_sdf(query_points, r, h, cylinder_center)

    # 使用阈值判断是否为内部体素
    threshold = 0  # 通常 SDF 小于 0 的值表示在物体内部
    primitive_inside = (sdf_cylinder < threshold)
    
    # 判断哪些点在物体内部
    object_inside = (sdf_object < threshold)

    # 计算交集和并集
    V_intersection = np.sum(primitive_inside & object_inside)  # 圆柱体和物体的交集
    V_union = np.sum(primitive_inside | object_inside)  # 圆柱体和物体的并集

    if V_union == 0:  # 避免除以 0
        return 0

    IoU = V_intersection / V_union  # 计算 IoU
    return IoU

# 模拟退火主循环
while T > T_min:
    # 生成邻域解
    r_new = r + random.uniform(-0.5, 0.5) * (0.05 * (1 - current_value) ** 2)
    h_new = h + random.uniform(-0.5, 0.5) * (0.05 * (1 - current_value) ** 2)
    t1_new = t1 + random.uniform(-0.5, 0.5) * (0.05 * (1 - current_value) ** 2)
    t2_new = t2 + random.uniform(-0.5, 0.5) * (0.05 * (1 - current_value) ** 2)
    t3_new = t3 + random.uniform(-0.5, 0.5) * (0.05 * (1 - current_value) ** 2)

    if r_new <= 0.001:
        r_new = 0.001
    if h_new <= 0.001:
        h_new = 0.001

    # 计算目标函数
    current_value = objective(r, h, t1, t2, t3)
    new_value = objective(r_new, h_new, t1_new, t2_new, t3_new)

    # 判断是否接受新解
    if new_value > current_value:
        r, h, t1, t2, t3 = r_new, h_new, t1_new, t2_new, t3_new

    # 降温
    T = alpha * T

    # 打印当前解和 IoU
    print(
      f"r={r}\n"
      f"h={h}\n"
      f"t1={t1}\n"
      f"t2={t2}\n"
      f"t3={t3}")

    print("IoU", current_value)
    print("nIoU", new_value)
