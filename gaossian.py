import numpy as np

# 参数设置
num_samples = 100000
image_size = 16

# 生成10000张16x16的高斯噪声图像
noise_images = np.random.normal(0, 1, (num_samples, image_size, image_size))

# 计算每个图像的DFT，并提取频域幅度
dft_magnitudes = np.zeros((num_samples, image_size, image_size))
for i in range(num_samples):
    # 进行二维傅里叶变换
    dft_image = np.fft.fft2(noise_images[i])
    magnitude = np.abs(dft_image)
    magnitude_shifted = np.fft.fftshift(magnitude)  # 将零频部分移到频谱图中心
    dft_magnitudes[i] = magnitude_shifted
# 统计每个频率点的幅度均值和方差
mean_magnitude = np.mean(dft_magnitudes, axis=0)
std_magnitude = np.std(dft_magnitudes, axis=0)

# 显示频域的均值和标准差
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

# 显示频域均值（幅度）
plt.subplot(1, 2, 1)
plt.imshow(mean_magnitude, cmap='gray')
plt.title('Mean Frequency Magnitude')
plt.colorbar()

# 显示标准差
plt.subplot(1, 2, 2)
plt.imshow(std_magnitude, cmap='gray')
plt.title('Standard Deviation of Magnitude')
plt.colorbar()

plt.tight_layout()
plt.show()
