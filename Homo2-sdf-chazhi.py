import numpy as np
import trimesh
from mesh_to_sdf import mesh_to_voxels
from mesh_to_sdf import mesh_to_sdf
import pyrender
import os
import sys
from scipy.ndimage import gaussian_filter
from skimage import measure  # 用于Marching Cubes算法
sys.path.append('/home/dermark/sdf')
from sdf import *

########################################################此文件用于物体同伦变换##################################


# 加载对象 mesh
# object_mesh = trimesh.load('/home/dermark/objtrans/kan.obj')
# object_mesh2 = trimesh.load('/home/dermark/objtrans/kan2.obj')
# ##############################################################elephant.obj IOU=0.55#######################################################
# x=0.0863899340038107
# y=0.05713638379041901
# w=0.0715346275314326
# t1=0.008668269074325463
# t2=-4.14762145262437e-05
# t3=0.008834076194377564
##############################################################duck.obj IOU=0.55#######################################################
x=0.07546296111470215
y=0.046540706229681955
w=0.08149108261265257
t1=-4.522645507427708e-05
t2=-0.002365694692405288
t3=-0.006804504741997466
##############################################################duck.obj IOU=0.55#######################################################
x=0.07
y=0.07
w=0.07
t1=0
t2=0
t3=0
##############################################################duck.obj IOU=0.55#######################################################
x=0.075
y=0.075
w=0.075
t1=0
t2=0
t3=0
##############################################################duck.obj IOU=0.55#######################################################
x=0.06
y=0.06
w=0.06
t1=0
t2=0
t3=0

size=[x, y, w]
transform=np.array([
            [1, 0, 0, t1],
            [0, 1, 0, t2],
            [0, 0, 1, t3],
            [0, 0, 0, 1]
        ])
object_mesh = trimesh.creation.box(extents=size,transform=transform)
# object_mesh.export('/home/dermark/objtrans/elephant_primitive.obj')
# object_mesh.export('/home/dermark/objtrans/duck_primitive.obj')
# object_mesh.export('/home/dermark/objtrans/duck_primitive.obj')
# object_mesh.export('/home/dermark/objtrans/duck_primitive.obj')
object_mesh.export('/home/dermark/objtrans/cube_006.obj')
#object_mesh=pyrender.Mesh.from_trimesh(cuboid,smooth=False)
# 加载对象 mesh
# object_mesh = trimesh.load('/home/dermark/objtrans/kan.obj')
# object_mesh2 = trimesh.load('/home/dermark/objtrans/grab/grabtestout/elephant.obj')
object_mesh2 = trimesh.load('/home/dermark/objtrans/grab/grabtestout/duck.obj')


volume_size=200
bounds_min, bounds_max = object_mesh2.bounds
bounds_min2,bounds_max2=object_mesh.bounds


# print("bounds_min, bounds_max",bounds_min, bounds_max)
# query_points = np.random.uniform(bounds_min, bounds_max, size=(volume_size**3, 3))

#query_points = np.random.uniform(-0.1, 0.1, size=(volume_size**3, 3))
# 计算两个 mesh 的 SDF





# grid_points = np.linspace(-0.1, 0.1, num=volume_size)
# x, y, z = np.meshgrid(grid_points, grid_points, grid_points)
# query_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

grid_points_x = np.linspace(bounds_min[0]-0.01, bounds_max[0]+0.01, num=volume_size)
grid_points_y = np.linspace(bounds_min[1]-0.01, bounds_max[1]+0.01, num=volume_size)
grid_points_z = np.linspace(bounds_min[2]-0.01, bounds_max[2]+0.01, num=volume_size)
x, y, z = np.meshgrid(grid_points_x, grid_points_y, grid_points_z)
query_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

voxels_kan2 = mesh_to_sdf(object_mesh2, query_points)
voxels_kan = mesh_to_sdf(object_mesh, query_points)

min_val, max_val = np.min(voxels_kan2), np.max(voxels_kan2)
print(f"Min: {min_val}, Max: {max_val}")
# 生成插值 SDF 并保存中间结果
n_steps = 20
for step in range(n_steps):
    alpha = step / (n_steps - 1)
    interpolated_sdf = (1 - alpha) * voxels_kan2 + alpha * voxels_kan
    bounds_minstep=(1 - alpha)*bounds_min+alpha *bounds_min2
    bounds_maxstep=(1 - alpha)*bounds_max+alpha *bounds_max2

    colors = np.zeros(query_points.shape)
    colors[interpolated_sdf < 0, 2] = 1
    colors[interpolated_sdf > 0, 0] = 1
    cloud = pyrender.Mesh.from_points(query_points, colors=colors)
    scene = pyrender.Scene()
    scene.add(cloud)
    viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)





    print("alpha",alpha)
    # 检查 interpolated_sdf 的最小值和最大值
    min_val, max_val = np.min(interpolated_sdf), np.max(interpolated_sdf)
    print(f"Min: {min_val}, Max: {max_val}")


    interpolated_sdf = interpolated_sdf.reshape((volume_size, volume_size, volume_size))

    voxels_cuboidfilt=gaussian_filter(interpolated_sdf, sigma=0.7)







    interpolated_sdf=voxels_cuboidfilt
    interpolated_sdf = np.transpose(interpolated_sdf, axes=(1, 0, 2))


    vertices, faces, normals, values = measure.marching_cubes(interpolated_sdf, level=0)
    # 使用 Trimesh 创建 mesh 对象
    # print("vertices",vertices.shape,vertices)



    # 获取 vertices 的最小值和最大值
    vertices_min = vertices.min(axis=0)
    vertices_max = vertices.max(axis=0)

    # 使用线性插值将顶点映射到新的范围
    vertices_rescaled = bounds_minstep + (vertices - vertices_min) / (vertices_max - vertices_min) * (bounds_maxstep - bounds_minstep)

    # 重新创建 mesh
    mesh_rescaled = trimesh.Trimesh(vertices=vertices_rescaled, faces=faces, vertex_normals=normals)

    # mesh2 = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)

    # 保存为 .obj 文件
    # output_filename = f'elephant_interpolated_step_{step}.obj'
    output_filename = f'duck_interpolated_step_{step}.obj'
    mesh_rescaled.export(output_filename)





