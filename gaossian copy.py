import numpy as np
import matplotlib.pyplot as plt

# 假设你生成了多个高斯噪声图像
num_images = 5  # 生成5张高斯噪声图像
image_size = 16

# 创建一个子图
fig, axes = plt.subplots(num_images, 2, figsize=(10, 10))

for i in range(num_images):
    # Step 1: 生成16x16的高斯噪声图像
    noise_image = np.random.normal(0, 1, (image_size, image_size))

    # Step 2: 绘制时域图像
    axes[i, 0].imshow(noise_image, cmap='gray')
    axes[i, 0].set_title(f'Time Domain: Noise Image {i+1}')
    axes[i, 0].axis('off')  # 去掉坐标轴

    # Step 3: 计算并绘制该图像的DFT
    dft_image = np.fft.fft2(noise_image)
    magnitude = np.abs(dft_image)
    magnitude_shifted = np.fft.fftshift(magnitude)  # 将零频部分移到中心

    # Step 4: 绘制频域图
    axes[i, 1].imshow(np.log(magnitude_shifted + 1), cmap='gray')  # 取对数显示
    axes[i, 1].set_title(f'Frequency Domain: DFT {i+1}')
    axes[i, 1].axis('off')  # 去掉坐标轴

plt.tight_layout()
plt.show()
