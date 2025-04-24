import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import math

# 设置随机种子保证可重复
torch.manual_seed(42)

# 超参数
num_samples = 1000
epochs = 200
lr = 0.01
lambda_l1 = 0  # L1 正则化的强度

# 遍历不同扰动尺度，从 0.01 到 10，步长为 0.01
random_scales = [round(0.01 * i, 2) for i in range(1, 1000)]
w2_final_values = []
w1_final_values = []
nan_indices = []

# 定义网络结构
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.w1 = nn.Parameter(torch.randn(1))
        self.w2 = nn.Parameter(torch.randn(1))
        self.w3 = nn.Parameter(torch.randn(1))

    def forward(self, x):
        y = x[:, 0] * self.w1 + x[:, 1] * self.w2
        z1 = y * self.w3
        return z1

# 遍历所有扰动尺度
for idx, scale in enumerate(random_scales):
    w2_val = float('nan')  # 默认设为 NaN
    w1_val = float('nan')
    try:
        x1 = scale * torch.randn(num_samples, 1)
        x2 = scale * torch.randn(num_samples, 1)
        x = torch.cat([x1, x2], dim=1)
        target = x1

        model = SimpleNet()
        optimizer = optim.SGD(model.parameters(), lr=lr)
        loss_fn = nn.MSELoss()

        for epoch in range(epochs):
            z1_pred = model(x)
            # 计算常规 MSE 损失
            loss = loss_fn(z1_pred, target)
            # 计算 L1 正则化项
            l1_norm = sum(torch.abs(param).sum() for param in model.parameters())
            # 将 L1 正则化项加到总损失上
            total_loss = loss + lambda_l1 * l1_norm

            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()

        w2_val = model.w2.item()
        w1_val = model.w1.item()

    except Exception:
        pass

    if math.isnan(w2_val):
        nan_indices.append(idx)
        w2_val = 1.0  # 用于图上红点表示

    w2_final_values.append(w2_val)
    w1_final_values.append(w1_val)

# 统计 w2 < 0.05 和 NaN
w2_small_count = sum(1 for w in w2_final_values if not math.isnan(w) and abs(w) < 0.05)
w2_nan_count = len(nan_indices)

# 输出统计
print(f"w2 < 0.05 count: {w2_small_count}")
print(f"NaN count: {w2_nan_count}")

# 绘制 w2 和 w1 的变化
fig, ax = plt.subplots(2, 1, figsize=(10, 12))

# 绘制 w2
ax[0].plot(random_scales, w2_final_values, marker='o', markersize=2, linewidth=1, label="w2 values")
ax[0].scatter([random_scales[i] for i in nan_indices], [1.0] * len(nan_indices), color='red', label='NaN (shown as 1.0)', s=10)
ax[0].set_xlabel("Random scale on x2")
ax[0].set_ylabel("Final value of w2")
ax[0].set_title("Final w2 vs x2 noise scale with L1 Regularization")
ax[0].grid(True)
ax[0].legend()

# 绘制 w1
ax[1].plot(random_scales, w1_final_values, marker='o', markersize=2, linewidth=1, label="w1 values")
ax[1].set_xlabel("Random scale on x2")
ax[1].set_ylabel("Final value of w1")
ax[1].set_title("Final w1 vs x2 noise scale with L1 Regularization")
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.show()
