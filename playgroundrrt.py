import numpy as np
import matplotlib.pyplot as plt

# 生成潜在变量 z
z_values = np.random.normal(size=(1000, 2))

# 绘制散点图
plt.scatter(z_values[:, 0], z_values[:, 1], alpha=0.5)
plt.xlabel("z1")
plt.ylabel("z2")
plt.title("Latent Space Distribution")
plt.show()
