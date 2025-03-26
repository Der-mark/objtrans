import numpy as np
import random
import trimesh
from mesh_to_sdf import mesh_to_sdf
import pyrender
########################################################此文件用于生成环的primitive##################################
# 加载对象 mesh
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/mug/mug.obj')
query_points = np.random.uniform(-0.2, 0.2, size=(125000, 3))
sdf_object = mesh_to_sdf(object_mesh, query_points)
# 初始解和温度
r1,r2, t1 = 0.03, 0.01,0.024
T = 1000
T_min = 1e-3
alpha = 0.99
current_value=0
# 目标函数：基于 SDF 计算 IoU
def objective(r1,r2, t1):
    
    transform = np.array([
        [1, 0, 0, t1],
        [0, 0, -1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
    cuboid = trimesh.creation.torus(major_radius=r1, minor_radius=r2,transform=transform)

    # 计算 SDF
    
    sdf_primitive = mesh_to_sdf(cuboid, query_points)
    

    # 使用阈值判断是否为内部体素
    threshold = 0  # 通常 SDF 小于 0 的值表示在物体内部
    primitive_inside = (sdf_primitive < threshold)
    object_inside = (sdf_object < threshold)

    # 计算交集和并集
    V_intersection = np.sum(primitive_inside & object_inside)
    V_union = np.sum(primitive_inside | object_inside)

    if V_union == 0:  # 避免除以 0
        return 0

    IoU = V_intersection / V_union
    return IoU

# 模拟退火主循环
while T > T_min:
    # 生成邻域解
    
    r1_new = r1 + random.uniform(-0.3, 0.3)*(0.05*(1-current_value)**2)
    r2_new = r2 + random.uniform(-0.1, 0.1)*(0.05*(1-current_value)**2)
    t1_new = t1 + random.uniform(-0.1, 0.1)*(0.05*(1-current_value)**2)
    if r1_new <= 0.001:
        r1_new = 0.001
    if r2_new <= 0.001:
        r2_new = 0.001
    

    # 计算目标函数
    current_value = objective(r1,r2, t1)
    new_value = objective(r1_new, r2_new ,t1_new)

    # 判断是否接受新解
    if new_value > current_value:
        r1, r2, t1 = r1_new, r2_new, t1_new
    
    # 降温
    T = alpha * T

    # 打印当前解和 IoU
    print(
      f"r1={r1}\n"
      f"r2={r2}\n"
      f"t1={t1}\n"
      )

    print("IOU", current_value)
    print("nIOU", new_value)
