import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # 用于计算欧几里得距离

# 读取 CSV 文件中的轨迹数据
df = pd.read_csv('/home/dermark/objtrans/data/end_effector_trajectory.csv')
df2 = pd.read_csv('/home/dermark/objtrans/data/sim/end_effector_trajectory.csv')

# 提取位置数据并转换为 mm
x_vals_real = df['x'].values * 1000
y_vals_real = df['y'].values * 1000
z_vals_real = df['z'].values * 1000

x_vals_sim = df2['x'].values * 1000
y_vals_sim = df2['y'].values * 1000
z_vals_sim = df2['z'].values * 1000

# 获取最后一帧的坐标
real_last = np.array([x_vals_real[-1], y_vals_real[-1], z_vals_real[-1]])
sim_last = np.array([x_vals_sim[-1], y_vals_sim[-1], z_vals_sim[-1]])

# 计算空间距离（欧几里得距离）
distance = np.linalg.norm(real_last - sim_last)

# 打印最后一帧的坐标和空间距离
print(f"Real last frame coordinates: {real_last}")
print(f"Simulated last frame coordinates: {sim_last}")
print(f"Distance between last frames: {distance} mm")

# 绘制 3D 轨迹
fig = plt.figure(figsize=(150, 150))  # 放大图形，设置尺寸为 15x15（原来的 5 倍）

ax = fig.add_subplot(111, projection='3d')

# 绘制真实数据轨迹
ax.plot(x_vals_real, y_vals_real, z_vals_real, label='Real End-Effector Trajectory', color='b')  # 蓝色

# 绘制模拟数据轨迹
ax.plot(x_vals_sim, y_vals_sim, z_vals_sim, label='Simulated End-Effector Trajectory', color='r')  # 红色

# 设置标签和标题
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('End-Effector Trajectories (in mm)')

# 获取 X, Y, Z 的范围
x_range = max(x_vals_real.max(), x_vals_sim.max()) - min(x_vals_real.min(), x_vals_sim.min())
y_range = max(y_vals_real.max(), y_vals_sim.max()) - min(y_vals_real.min(), y_vals_sim.min())
z_range = max(z_vals_real.max(), z_vals_sim.max()) - min(z_vals_real.min(), z_vals_sim.min())

# 设置相同的比例范围以确保刻度等长
max_range = max(x_range, y_range, z_range)

# 设置坐标轴的范围
ax.set_xlim([min(x_vals_real.min(), x_vals_sim.min()) ,
             max(x_vals_real.max(), x_vals_sim.max()) ])
ax.set_ylim([min(y_vals_real.min(), y_vals_sim.min()) ,
             max(y_vals_real.max(), y_vals_sim.max()) ])
ax.set_zlim([min(z_vals_real.min(), z_vals_sim.min()) ,
             max(z_vals_real.max(), z_vals_sim.max()) ])

# 显示图例
ax.legend()

# 显示图形
plt.show()
