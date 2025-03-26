import os
##################################################生成seed的空文件夹##################################
# Define the base directory
base_directory = "/home/dermark/Uni_leap/dexgrasp/logs/shadow_hand_grasp_fly_leap/ppo"
base_directory = "/home/dermark/UniDexGrasp2/dexgrasp/logs/fly_leap_track_hbh_generalist/ppo"
base_directory = "/home/dermark/LeapHandGrasp-Der/runs"

# Create directories for seeds 47 to 100
for seed in range(300, 800):
    directory_path = os.path.join(base_directory, f"ppo_seed{seed}")
    os.makedirs(directory_path, exist_ok=True)

print("Directories for seeds 47 to 100 created successfully.")