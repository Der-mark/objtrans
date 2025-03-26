import re
########################################################此文件用于生成object list文件名##################################
# 给定的文件路径列表
npy_file_list = [
            'data/hechengtest1/passive_active_info_ori_grab_s2_cup_drink_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s7_flashlight_pass_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_hammer_use_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_apple_lift_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_hammer_use_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_mouse_pass_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_toothpaste_squeeze_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s1_lightbulb_pass_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s1_stamp_pass_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_toothpaste_squeeze_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_phone_pass_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s7_flashlight_pass_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_mouse_pass_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_apple_lift_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_cup_drink_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_toothpaste_squeeze_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_cubesmall_inspect_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_cubesmall_inspect_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_flute_pass_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s7_flashlight_pass_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_cubesmall_inspect_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_phone_pass_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_cup_drink_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_apple_lift_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s1_lightbulb_pass_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s1_stamp_pass_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_flute_pass_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s1_stamp_pass_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_flute_pass_1_nf_300_sample_1.npy',
'data/hechengtest1/passive_active_info_ori_grab_s1_lightbulb_pass_1_nf_300_sample_2.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_mouse_pass_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_phone_pass_1_nf_300_sample_0.npy',
'data/hechengtest1/passive_active_info_ori_grab_s2_hammer_use_1_nf_300_sample_1.npy'
]

# 创建新的路径列表
urdf_file_list = []

# 提取物体名称并生成新路径
for npy_file in npy_file_list:
    # 使用正则表达式提取文件路径中的物体名称
    match = re.search(r'passive_active_info_ori_grab_s\d+_([a-zA-Z0-9]+)', npy_file)
    
    if match:
        object_name = match.group(1)  # 提取到的物体名称
        urdf_path = f"urdf/objects/GRAB/{object_name}/{object_name}.urdf"  # 格式化为urdf路径
        urdf_file_list.append(urdf_path)  # 添加到新列表中

# 打印输出生成的urdf路径列表
for urdf in urdf_file_list:
    print("'"+urdf+"',")