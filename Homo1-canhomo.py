import numpy as np
import trimesh
from mesh_to_sdf import mesh_to_voxels
from mesh_to_sdf import mesh_to_sdf
from mesh_to_sdf import sample_sdf_near_surface
from scipy.ndimage import gaussian_filter
import trimesh
import pyrender
import numpy as np
from skimage import measure  # 用于Marching Cubes算法
import pyrender
import os
########################################################此文件用于物体同伦变换##################################
# 计算两个 mesh 的 SDF
object_mesh = trimesh.load('/home/dermark/objtrans/objfile/Milkbottle.obj')
x = 0.049926478827075266
y = 0.03772258393173206
w = 0.1103478189225535
t1 = -0.0006408552331349965
t2 = 8.231149127958601e-06
t3 = -0.017834210012684426

size = [x, y, w]
transform = np.array([
    [1, 0, 0, t1],
    [0, 1, 0, t2],
    [0, 0, 1, t3],
    [0, 0, 0, 1]
])
cuboid = trimesh.creation.box(extents=size, transform=transform)
cuboid = cuboid.subdivide()
cuboid = cuboid.subdivide()
#query_points = np.random.uniform(-0.2, 0.2, size=(250047, 3))


##################################################################################################
points, sdf = sample_sdf_near_surface(object_mesh, number_of_points=250000)

colors = np.zeros(points.shape)
colors[sdf < 0, 2] = 1
colors[sdf > 0, 0] = 1
cloud = pyrender.Mesh.from_points(points, colors=colors)
scene = pyrender.Scene()
scene.add(cloud)
viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)

##################################################################################################
#voxels_cuboid = mesh_to_sdf(cuboid, query_points)
#voxels_object = mesh_to_sdf(object_mesh, query_points)
#kansdf=voxels_cuboid
kansdf=sdf
#kansdf2=voxels_object
volume_size=100
#kansdf = kansdf.reshape((volume_size, volume_size, volume_size))
#kansdf2 = kansdf2.reshape((volume_size, volume_size, volume_size))


grid_points = np.linspace(-0.1, 0.1, num=volume_size)







x, y, z = np.meshgrid(grid_points, grid_points, grid_points)
query_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T
voxels_cuboid = mesh_to_sdf(cuboid, query_points)


voxels_cuboid = voxels_cuboid.reshape((volume_size, volume_size, volume_size))
voxels_cuboidfilt=gaussian_filter(voxels_cuboid, sigma=0.7)


vertices2, faces2, normals2, values2 = measure.marching_cubes(voxels_cuboidfilt, level=0)
# 使用 Trimesh 创建 mesh 对象
mesh = trimesh.Trimesh(vertices=vertices2, faces=faces2, vertex_normals=normals2)





grid_points = np.linspace(-0.1, 0.1, num=volume_size)
x, y, z = np.meshgrid(grid_points, grid_points, grid_points)
query_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T



voxels_cuboid2 = mesh_to_sdf(object_mesh, query_points)
voxels_cuboid2 = voxels_cuboid2.reshape((volume_size, volume_size, volume_size))



vertices, faces, normals, values = measure.marching_cubes(voxels_cuboid2, level=0)
# 使用 Trimesh 创建 mesh 对象
mesh2 = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)

# 保存为 .obj 文件
output_filename = f'kan2.obj'
mesh2.export(output_filename)




# 保存为 .obj 文件
output_filename = f'kan.obj'
mesh.export(output_filename)
# 生成插值 SDF 并保存中间结果
# n_steps = 5
# for step in range(n_steps):
#     alpha = step / (n_steps - 1)
#     interpolated_sdf = (1 - alpha) * voxels_cuboid + alpha * voxels_object

#     # 将 SDF 转换为体素网格（例如使用 Marching Cubes）
#     volume_size = 63  # 假设 SDF 是 50x50x50 的三维网格
#     interpolated_sdf = interpolated_sdf.reshape((volume_size, volume_size, volume_size))

#     # 使用 Marching Cubes 从 SDF 生成网格
#     vertices, faces, normals, values = measure.marching_cubes(interpolated_sdf, level=0)

#     # 使用 Trimesh 创建 mesh 对象
#     mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)

#     # 保存为 .obj 文件
#     output_filename = f'interpolated_step_{step}.obj'
#     mesh.export(output_filename)
