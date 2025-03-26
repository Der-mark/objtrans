import numpy as np
import random
import trimesh
from mesh_to_sdf import mesh_to_sdf
import pyrender
########################################################此文件用于寻找最大IOU的cube prim##################################
# 加载对象 mesh
object_mesh = trimesh.load('/home/dermark/objtrans/objfile/Milkbottle.obj')
object_mesh2 = trimesh.load('/home/dermark/objtrans/objfile/bear082.obj')
query_points = np.random.uniform(-0.1, 0.1, size=(250000, 3))
sdf_object = mesh_to_sdf(object_mesh2, query_points)
# 初始解和温度
x, y, w, t1, t2, t3 = 0.01*random.uniform(1, 5), 0.01*random.uniform(1, 5), 0.01*random.uniform(1, 5), 0.01*random.uniform(-1, 1), 0.01*random.uniform(-1, 1), 0.01*random.uniform(-1, 1)
T = 1000
T_min = 1e-3
alpha = 0.99
current_value=0
times=0
the_bigest_number=2000
# 目标函数：基于 SDF 计算 IoU
def objective(x, y, w, t1, t2, t3):
    size = [x, y, w]
    transform = np.array([
        [1, 0, 0, t1],
        [0, 1, 0, t2],
        [0, 0, 1, t3],
        [0, 0, 0, 1]
    ])
    cuboid = trimesh.creation.box(extents=size, transform=transform)

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
while times<=the_bigest_number:
    # 生成邻域解
    
    x_new = x + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    y_new = y + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    w_new = w + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    t1_new = t1 + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    t2_new = t2 + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    t3_new = t3 + random.uniform(-0.5, 0.5)*(0.05*(1-current_value)**2)
    if x_new <= 0.01:
        x_new = 0.01
    if y_new <= 0.01:
        y_new = 0.01
    if w_new <= 0.01:
        w_new = 0.01

    # 计算目标函数
    current_value = objective(x, y, w, t1, t2, t3)
    new_value = objective(x_new, y_new, w_new, t1_new, t2_new, t3_new)

    # 判断是否接受新解
    if new_value > current_value:
        x, y, w, t1, t2, t3 = x_new, y_new, w_new, t1_new, t2_new, t3_new
    
    times=times+1

    # 打印当前解和 IoU
    print(f"x={x}\n"
      f"y={y}\n"
      f"w={w}\n"
      f"t1={t1}\n"
      f"t2={t2}\n"
      f"t3={t3}")

    print("IOU", current_value)
    print("nIOU", new_value)
    print("times", times)
