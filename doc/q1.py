import numpy as np

# 给定参数
e = 2.06136076e-3
h = 5.23308462e4  # km^2/s
Omega = 5.69987423  # rad
i = 1.69931232      # rad
omega = 4.10858621  # rad
theta = 3.43807372  # rad
mu = 398600.4418    # km^3/s^2

# 步骤1：计算半长轴 a
a = h**2 / (mu * (1 - e**2))

# 步骤2：计算距离 r
r = h**2 / mu / (1 + e * np.cos(theta))

# 步骤3：位置向量在轨道平面内的坐标
x_p = r * np.cos(theta)
y_p = r * np.sin(theta)

# 步骤4：速度向量在轨道平面内的坐标
v_xp = -mu / h * np.sin(theta)
v_yp = mu / h * (e + np.cos(theta))

# 步骤5：构建旋转矩阵
R_z_Omega = np.array([
    [np.cos(-Omega), np.sin(-Omega), 0],
    [-np.sin(-Omega), np.cos(-Omega), 0],
    [0, 0, 1]
])

R_x_i = np.array([
    [1, 0, 0],
    [0, np.cos(-i), np.sin(-i)],
    [0, -np.sin(-i), np.cos(-i)]
])

R_z_omega = np.array([
    [np.cos(-omega), np.sin(-omega), 0],
    [-np.sin(-omega), np.cos(-omega), 0],
    [0, 0, 1]
])

R = R_z_Omega @ R_x_i @ R_z_omega

# 步骤6：应用旋转矩阵转换到GCRS坐标系
position_perifocal = np.array([x_p, y_p, 0])
velocity_perifocal = np.array([v_xp, v_yp, 0])

position_gcrs = R @ position_perifocal
velocity_gcrs = R @ velocity_perifocal

# 输出结果
print("位置 (km):", position_gcrs)
print("速度 (km/s):", velocity_gcrs)

