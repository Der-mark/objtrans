import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件中的轨迹数据
df = pd.read_csv('/home/dermark/objtrans/data/qtarget_trajectory.csv')
df2 = pd.read_csv('/home/dermark/objtrans/data/sim/qtarget_trajectory.csv')

# 获取 DOF 数据（0 到 5）
qpos_real = df[['q0', 'q1', 'q2', 'q3', 'q4', 'q5']].values  # 真实数据
qpos_sim = df2[['q0', 'q1', 'q2', 'q3', 'q4', 'q5']].values  # 模拟数据

# 创建 6 个子图，分别画每个 DOF 的轨迹
fig, axes = plt.subplots(3, 2, figsize=(12, 10))  # 创建 3x2 的子图布局

# 绘制每个 DOF 的轨迹
for i in range(6):
    # 获取当前 DOF 的数据
    ax = axes[i // 2, i % 2]  # 选择对应的子图位置
    ax.plot(qpos_real[:, i], label=f'Real DOF {i}', color='b')  # 真实数据，蓝色
    ax.plot(qpos_sim[:, i], label=f'Simulated DOF {i}', color='r')  # 模拟数据，红色
    ax.set_title(f'DOF {i} velTrajectory')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Velocity')
    ax.legend()

# 调整子图布局
plt.tight_layout()

# 显示图形
plt.show()

