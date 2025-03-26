import numpy as np
import trimesh
from mesh_to_sdf import mesh_to_voxels
from mesh_to_sdf import mesh_to_sdf
import pyrender
import os
import sys
from skimage import measure  # 用于Marching Cubes算法
sys.path.append('/home/dermark/sdf')
from sdf import *
########################################################此文件用于物体同伦变换##################################

# 加载对象 mesh
# object_mesh = trimesh.load('/home/dermark/objtrans/kan.obj')
# object_mesh2 = trimesh.load('/home/dermark/objtrans/kan2.obj')




x=0.0863899340038107
y=0.05713638379041901
w=0.0715346275314326
t1=0.008668269074325463
t2=-4.14762145262437e-05
t3=0.008834076194377564



size=[x, y, w]
transform=np.array([
            [1, 0, 0, t1],
            [0, 1, 0, t2],
            [0, 0, 1, t3],
            [0, 0, 0, 1]
        ])
object_mesh = trimesh.creation.box(extents=size,transform=transform)
#object_mesh=pyrender.Mesh.from_trimesh(cuboid,smooth=False)
# 加载对象 mesh
# object_mesh = trimesh.load('/home/dermark/objtrans/kan.obj')
object_mesh2 = trimesh.load('/home/dermark/objtrans/grab/grabtestout/elephant.obj')







volume_size = 100
bounds_min, bounds_max = object_mesh2.bounds
bounds_min2, bounds_max2 = object_mesh.bounds

# 生成采样点的网格
grid_points_x = np.linspace(bounds_min[0] - 1, bounds_max[0] + 1, num=volume_size)
grid_points_y = np.linspace(bounds_min[1] - 1, bounds_max[1] + 1, num=volume_size)
grid_points_z = np.linspace(bounds_min[2] - 1, bounds_max[2] + 1, num=volume_size)
x, y, z = np.meshgrid(grid_points_x, grid_points_y, grid_points_z)
query_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

voxels_kan2 = mesh_to_sdf(object_mesh2, query_points)
voxels_kan = mesh_to_sdf(object_mesh, query_points)

# 生成插值 SDF 并保存中间结果
n_steps = 5
scene = pyrender.Scene()  # 创建场景



for step in range(n_steps):
    alpha = step / (n_steps - 1)
    interpolated_sdf = (1 - alpha) * voxels_kan2 + alpha * voxels_kan
    bounds_minstep = (1 - alpha) * bounds_min + alpha * bounds_min2
    bounds_maxstep = (1 - alpha) * bounds_max + alpha * bounds_max2

    interpolated_sdf = interpolated_sdf.reshape((volume_size, volume_size, volume_size))

    # 反向 SDF 以获得内部
    interpolated_sdf = interpolated_sdf
    # 对 SDF 进行转置，使方向正确
    interpolated_sdf = np.transpose(interpolated_sdf, axes=(1, 0, 2))

    vertices, faces, normals, values = measure.marching_cubes(interpolated_sdf, level=0)

    # 获取 vertices 的最小值和最大值
    vertices_min = vertices.min(axis=0)
    vertices_max = vertices.max(axis=0)

    # 使用线性插值将顶点映射到新的范围
    vertices_rescaled = bounds_minstep + (vertices - vertices_min) / (vertices_max - vertices_min) * (bounds_maxstep - bounds_minstep)

    # 平移每个对象，以便它们沿 X 轴从左到右排列
    translation = np.array([step * (bounds_max[0] - bounds_min[0] + 5), 0, 0])  # 每个对象之间间隔5个单位长度
    vertices_rescaled += translation

    # 创建 mesh
    mesh_rescaled = trimesh.Trimesh(vertices=vertices_rescaled, faces=faces, vertex_normals=None)



    mesh_pyrender = pyrender.Mesh.from_trimesh(mesh_rescaled)
    scene.add(mesh_pyrender)

# 设置相机参数
camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
camera_pose = np.array([
    [1.0, 0.0, 0.0, 3],
    [0.0, 1.0, 0.0, -1],
    [0.0, 0.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 1.0]
])
scene.add(camera, pose=camera_pose)

# 使用 OffscreenRenderer 拍摄图像
r = pyrender.OffscreenRenderer(viewport_width=640, viewport_height=480)
color, depth = r.render(scene)

# 保存图片
from PIL import Image
img = Image.fromarray(color)
img.save('scene_snapshot.png')
r.delete()

# 可视化所有步骤的 mesh
viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)  
