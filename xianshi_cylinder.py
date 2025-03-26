import numpy as np
import random
import numpy as np
import trimesh
from mesh_to_sdf import mesh_to_voxels
import pyrender
import time
#####################################################此文件用于画图，cylinder primitive和原object##################################
# 加载对象 mesh
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/waterbottle/waterbottle.obj')
object_mesh = trimesh.load('/home/dermark/objtrans/grab/grabtestout/flashlight/flashlight.obj')
voxels_object = mesh_to_voxels(object_mesh, 30, pad=True)
# 初始解和温度

##############################################################waterbottle.obj IOU=0.85#######################################################
r=0.03006322809568718
h=0.10536885749915195
t1=-0.00046808035236275367
t2=1.8501342158268086e-05
t3=-0.005360844683445518
##############################################################flashlight.obj IOU=0.55###################################################
r=0.01
h=0.12515415301411698
t1=0.0008870596944968241
t2=-0.0007119996401248579
t3=0.01045270039561799

r=0.01022457363728245
h=0.09969080945565804
t1=8.365826866859997e-05
t2=-0.0008286686643460719
t3=0.01926940612669072


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
cuboid = trimesh.creation.cylinder(radius=r, height=h,transform=transform)


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

# output_file = '/home/dermark/objtrans/grab/grabtestout/waterbottle/waterbottle_primitive.obj'
# cuboid.export(output_file)

# print(f"Model has been saved to {output_file}")

