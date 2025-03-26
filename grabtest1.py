import trimesh
import os
########################################################此文件用于创造obj文件以及其urdf##################################
# 输入目录路径
input_dir = "/home/dermark/GRAB/tools/object_meshes/contact_meshes"
output_dir = "/home/dermark/objtrans/grab/grabtestout_ddd"

# 获取文件夹下所有 ply 文件
ply_files = [f for f in os.listdir(input_dir) if f.endswith('.ply')]

# 批量加载并转换为 obj 文件
for ply_file in ply_files:
    ply_path = os.path.join(input_dir, ply_file)  # 拼接成完整的 ply 文件路径
    mesh = trimesh.load(ply_path)  # 加载 ply 文件

    # 获取文件名（不包含扩展名）
    file_name_without_extension = os.path.splitext(ply_file)[0]

    # 创建新的子文件夹路径
    subfolder_path = os.path.join(output_dir, file_name_without_extension)

    # 如果子文件夹不存在，则创建它
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    # 拼接 obj 文件的完整路径
    obj_filename = file_name_without_extension + '.obj'
    obj_path = os.path.join(subfolder_path, obj_filename)

    # 导出为 obj 文件
    mesh.export(obj_path)

    print(f"Converted {ply_file} to {obj_filename} and saved in {subfolder_path}")




# 获取所有子文件夹（每个子文件夹对应一个对象）
subfolders = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]

# URDF 文件模板
# urdf_template = '''<robot name="root">
#   <link name="link_001">
#     <visual>
#       <origin xyz="0 0 0" rpy="0 0 0"/>
#       <geometry>
#         <mesh filename="{mesh_filename}" scale="1.0000E+00 1.0000E+00 1.0000E+00"/>
#       </geometry>
#       <material name="">
#         <color rgba="7.50E-01 7.50E-01 7.50E-01 1"/>
#       </material>
#     </visual>
#     <collision>
#       <origin xyz="0 0 0" rpy="0 0 0"/>
#       <geometry>
#         <mesh filename="{mesh_filename}" scale="1.0000E+00 1.0000E+00 1.0000E+00"/>
#       </geometry>
#     </collision>
#     <inertial>
#       <mass value="0.16"/> <!-- 质量：0.1kg -->
#     </inertial>
#   </link>
# </robot>
# '''
urdf_template = '''<robot name="root">
  <link name="link_001">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="{mesh_filename}" scale="0.600E+00 0.600E+00 0.6000E+00"/>
      </geometry>
      <material name="">
        <color rgba="7.50E-01 7.50E-01 7.50E-01 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="{mesh_filename}" scale="0.6000E+00 0.6000E+00 0.6000E+00"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.16"/> <!-- 质量：0.1kg -->
    </inertial>
  </link>
</robot>
'''

# 遍历每个子文件夹，创建对应的 URDF 文件
for subfolder in subfolders:
    # 获取子文件夹路径
    subfolder_path = os.path.join(output_dir, subfolder)
    
    # 创建 URDF 文件路径
    urdf_filename = f"{subfolder}.urdf"
    urdf_filepath = os.path.join(subfolder_path, urdf_filename)
    
    # 替换 URDF 模板中的 mesh_filename 为当前子文件夹的名称
    mesh_filename = f"{subfolder}.obj"  # 假设 OBJ 文件与子文件夹名称相同
    urdf_content = urdf_template.format(mesh_filename=mesh_filename)
    
    # 将 URDF 内容写入文件
    with open(urdf_filepath, 'w') as urdf_file:
        urdf_file.write(urdf_content)
    
    print(f"Created URDF file for {subfolder} at {urdf_filepath}")