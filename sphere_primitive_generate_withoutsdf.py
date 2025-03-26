import numpy as np
import random
import trimesh
from mesh_to_sdf import mesh_to_sdf
import pyrender
#####################################################此文件用于无sdf找到球体primitive##################################
# 加载目标网格对象
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/stanfordbunny/stanfordbunny.obj')

# 生成随机查询点（用于计算 SDF）
query_points = np.random.uniform(-0.2, 0.2, size=(125000, 3))

# 使用 mesh_to_sdf 获取目标网格的 SDF
sdf_object = mesh_to_sdf(object_mesh, query_points)

# 初始解和温度
r = 0.01 * random.uniform(2, 10)
t1, t2, t3 = 0.01 * random.uniform(-1, 1), 0.01 * random.uniform(-1, 1), 0.01 * random.uniform(-1, 1)
T = 1000
T_min = 1e-3
alpha = 0.99
current_value = 0

# 计算球体的 SDF
def sphere_sdf(points, radius, center):
    """计算球体的 SDF"""
    return np.linalg.norm(points - center, axis=1) - radius

# 目标函数：基于 SDF 计算 IoU
def objective(r, t1, t2, t3):
    # 球体 SDF计算
    sphere_center = np.array([t1, t2, t3])
    sdf_sphere = sphere_sdf(query_points, r, sphere_center)

    # 计算交集与并集
    # 交集：球体内且网格内
    primitive_inside = sdf_sphere < 0
    object_inside = sdf_object < 0
    
    # 并集：球体内或网格内
    V_intersection = np.sum(primitive_inside & object_inside)
    V_union = np.sum(primitive_inside | object_inside)

    if V_union == 0:  # 避免除以 0
        return 0

    IoU = V_intersection / V_union
    return IoU

# 模拟退火主循环
while T > T_min:
    # 生成邻域解
    r_new = r + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    t1_new = t1 + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    t2_new = t2 + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    t3_new = t3 + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    
    if r_new <= 0.01:
        r_new = 0.01

    # 计算目标函数
    current_value = objective(r, t1, t2, t3)
    new_value = objective(r_new, t1_new, t2_new, t3_new)

    # 判断是否接受新解
    if new_value > current_value:
        r, t1, t2, t3 = r_new, t1_new, t2_new, t3_new
    
    # 降温
    T = alpha * T

    # 打印当前解和 IoU
    print(f"r={r}\nt1={t1}\nt2={t2}\nt3={t3}")
    print("IoU", current_value)
    print("nIoU", new_value)
