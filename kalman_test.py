import torch
import numpy as np
import matplotlib.pyplot as plt

# 定义卡尔曼滤波器类
class KalmanFilter:
    def __init__(self, state_dim, observation_dim, dt):
        self.state_dim = state_dim
        self.observation_dim = observation_dim
        self.dt = dt

        # 初始化状态（位置和速度）
        self.x = torch.zeros(state_dim)  # [position, velocity]
        
        # 初始误差协方差矩阵
        self.P = torch.eye(state_dim) * 1000  # 高初始误差

        # 状态转移矩阵 (A)，位置由速度决定
        self.A = torch.eye(state_dim)
        self.A[0, 1] = self.dt  # 位置变化由速度决定

        # 控制输入矩阵 (B)，此处假设不使用
        self.B = torch.zeros((state_dim, 1))

        # 观测矩阵 (H)，假设直接观测位置和速度
        self.H = torch.eye(state_dim)

        # 过程噪声协方差矩阵 (Q)
        self.Q = torch.eye(state_dim) * 0.01  # 过程噪声

        # 观测噪声协方差矩阵 (R)
        self.R = torch.eye(observation_dim) * 0.5  # 观测噪声

    def predict(self):
        self.x = torch.matmul(self.A, self.x)  # 预测位置和速度
        self.P = torch.matmul(self.A, torch.matmul(self.P, self.A.T)) + self.Q  # 更新协方差矩阵

    def update(self, z):
        y = z - torch.matmul(self.H, self.x)  # 观测残差
        S = torch.matmul(self.H, torch.matmul(self.P, self.H.T)) + self.R  # 观测残差的协方差
        K = torch.matmul(self.P, torch.matmul(self.H.T, torch.inverse(S)))  # 卡尔曼增益

        # 更新状态和协方差矩阵
        self.x = self.x + torch.matmul(K, y)
        self.P = self.P - torch.matmul(K, torch.matmul(self.H, self.P))

    def get_state(self):
        return self.x

# 模拟真实的运动轨迹（例如，位置和速度）
time_steps = 100
true_position = torch.zeros(time_steps)
true_velocity = torch.zeros(time_steps)

# 模拟初始位置和速度
true_position[0] = 0
true_velocity[0] = 1  # 初始速度

# 模拟运动轨迹，假设速度为常数，位置为线性变化
for t in range(1, time_steps):
    true_position[t] = true_position[t-1] + true_velocity[t-1] * 0.1  # 位置变化
    true_velocity[t] = true_velocity[t-1]  # 速度不变（简单模拟）

# 添加噪声到观测值
noise_position = torch.randn(time_steps) * 0.05  # 添加位置噪声
noise_velocity = torch.randn(time_steps) * 0.2  # 添加速度噪声
observed_position = true_position + noise_position
observed_velocity = true_velocity + noise_velocity

# 初始化卡尔曼滤波器
kf = KalmanFilter(state_dim=2, observation_dim=2, dt=0.1)  # 2D 状态：位置和速度

# 用于存储滤波后的估计值
filtered_positions = []
filtered_velocities = []

# 进行卡尔曼滤波
for t in range(time_steps):
    z = torch.tensor([observed_position[t], observed_velocity[t]])  # 当前观测值
    kf.predict()  # 预测
    kf.update(z)  # 更新
    state_estimate = kf.get_state()  # 获取滤波后的状态

    # 存储估计值
    filtered_positions.append(state_estimate[0].item())
    filtered_velocities.append(state_estimate[1].item())

# 可视化结果
plt.figure(figsize=(10, 6))

# 绘制位置图
plt.subplot(2, 1, 1)
plt.plot(true_position.numpy(), label='True Position', linestyle='-', color='g')
plt.plot(observed_position.numpy(), label='Observed Position', linestyle='--', color='r')
plt.plot(filtered_positions, label='Filtered Position (Kalman)', linestyle='-', color='b')
plt.title('Position Estimation')
plt.legend()

# 绘制速度图
plt.subplot(2, 1, 2)
plt.plot(true_velocity.numpy(), label='True Velocity', linestyle='-', color='g')
plt.plot(observed_velocity.numpy(), label='Observed Velocity', linestyle='--', color='r')
plt.plot(filtered_velocities, label='Filtered Velocity (Kalman)', linestyle='-', color='b')
plt.title('Velocity Estimation')
plt.legend()

plt.tight_layout()
plt.show()
