import numpy as np
import random
import numpy as np
import trimesh
from mesh_to_sdf import mesh_to_voxels
import pyrender
import time
#####################################################此文件用于画图，ring primitive和原object##################################
# 加载对象 mesh
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/mug/mug.obj')
voxels_object = mesh_to_voxels(object_mesh, 30, pad=True)
# 初始解和温度

##############################################################mug.obj IOU=0.05#######################################################
r1=0.03916953592359328
r2=0.008981290161180593
t1=0.02177906989869799
r1=0.046283247191516726
r2=0.010816698597708447
t1=0.018510055040169445
# r1=0.034711361856383904
# r2=0.013768967210576619
# t1=0.014209711993012297
# r1=0.046283247191516726
# r2=0.010816698597708447
# t1=0.018510055040169445
# r1=0.03911836657700861
# r2=0.014644198493995744
# t1=0.013413340914796387
# r1=0.05360923067023439
# r2=0.014318538416088884
# t1=0.006342405930606931
r1=0.04495271721048496
r2=0.005162737282101836
t1=0.009912068278225241

transform=np.array([
            [1, 0, 0, t1],
            [0, 0, -1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])


# 创建 pyrender 场景
scene = pyrender.Scene()
camera = pyrender.PerspectiveCamera(yfov=np.pi / 2)
camera_pose = np.array([
    [1.0, 0.0, 0.0, 0],
    [0.0, 1.0, 0.0, 0],
    [0.0, 0.0, 1.0, 2.0],
    [0.0, 0.0, 0.0, 1.0]
])
scene.add(camera, pose=camera_pose)
cuboid = trimesh.creation.torus(major_radius=r1, minor_radius=r2,transform=transform)


#cuboid=trimesh.load('/home/dermark/objtrans/kan2.obj')

# 为透明物体设置材质并启用 alpha 混合
material = pyrender.MetallicRoughnessMaterial(
    baseColorFactor=(1.0, 0.0, 0.0, 0.2),  # 半透明红色
    alphaMode='BLEND'  # 启用透明度混合
)

material2 = pyrender.MetallicRoughnessMaterial(
    baseColorFactor=(0.0, 1.0, 1.0, 0.2),  # 半透明红色
    alphaMode='BLEND'  # 启用透明度混合
)
#object_pyrender = pyrender.Mesh.from_trimesh(object_mesh,material=material)



mesh=pyrender.Mesh.from_trimesh(cuboid, material=material2,smooth=False)
mesh_node = scene.add(mesh)
objectt=pyrender.Mesh.from_trimesh(object_mesh, material=material,smooth=False)
obj_node = scene.add(objectt)





viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2, run_in_thread=True,render_transparent=True)


