import numpy as np
import random
import numpy as np
import trimesh
from mesh_to_sdf import mesh_to_voxels
import pyrender
import time
#####################################################此文件用于画图，sphere primitive和原object##################################
# 加载对象 mesh
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/apple/apple.obj')
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/stanfordbunny/stanfordbunny.obj')
voxels_object = mesh_to_voxels(object_mesh, 30, pad=True)
# 初始解和温度

##############################################################apple.obj IOU=0.87#######################################################
r=0.04346593743383691
t1=-0.0016064627009372218
t2=8.364390530810382e-05
t3=-0.00683190528806545
##############################################################apple.obj IOU=0.8997#######################################################
r=0.0435599015367148
t1=-0.0005563558461653845
t2=-0.000188097901602874
t3=-0.007199625125286523

##############################################################bunny.obj IOU=0.63#######################################################
r=0.044853423509869976
t1=0.006537169712067631
t2=-0.012707931875992225
t3=-0.02870269727030702


transform=np.array([
            [1, 0, 0, t1],
            [0, 1, 0, t2],
            [0, 0, 1, t3],
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
cuboid = trimesh.creation.uv_sphere(radius=r, transform=transform)


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


# output_file = '/home/dermark/objtrans/grab/grabtestout/apple/apple_primitive.obj'
# cuboid.export(output_file)

# print(f"Model has been saved to {output_file}")