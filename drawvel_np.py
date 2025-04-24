import pandas as pd
import matplotlib.pyplot as plt

# 读取保存的 CSV 文件
df = pd.read_csv('robot_delta_states_weights_np_vel.csv')

# 绘制图形
plt.figure(figsize=(10, 6))
plt.subplot(2, 3, 1)
plt.plot(df['X'])
plt.title('X')

plt.subplot(2, 3, 2)
plt.plot(df['Y'])
plt.title('Y')

plt.subplot(2, 3, 3)
plt.plot(df['Z'])
plt.title('Z')

plt.subplot(2, 3, 4)
plt.plot(df['Roll'])
plt.title('Roll')

plt.subplot(2, 3, 5)
plt.plot(df['Pitch'])
plt.title('Pitch')

plt.subplot(2, 3, 6)
plt.plot(df['Yaw'])
plt.title('Yaw')

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
