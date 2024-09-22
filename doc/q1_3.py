import numpy as np

# 给定参数
e = 2.06136076e-3  # 偏心率
h = 5.23308462e4    # 角动量 km^2/s
Omega = 5.69987423  # 升交点赤经 rad
i = 1.69931232      # 轨道倾角 rad
omega = 4.10858621  # 近地点幅角 rad
theta = 3.43807372  # 真近点角 rad
mu = 398600.4418    # 地球引力常数 km^3/s^2

# 步骤1：计算半长轴 a
a = h**2 / (mu * (1 - e**2))
print(f"半长轴 a: {a:.6f} km")

# 步骤2：计算距离 r
r = (h**2 / mu) / (1 + e * np.cos(theta))
print(f"距离 r: {r:.6f} km")

# 步骤3：位置向量在轨道平面内的坐标
x_p = r * np.cos(theta)
y_p = r * np.sin(theta)
print(f"轨道平面内位置坐标 x_p: {x_p:.6f} km, y_p: {y_p:.6f} km")

# 步骤4：速度向量在轨道平面内的坐标
v_xp = -mu / h * np.sin(theta)
v_yp = mu / h * (e + np.cos(theta))
print(f"轨道平面内速度坐标 v_xp: {v_xp:.6f} km/s, v_yp: {v_yp:.6f} km/s")

# 步骤5：构建旋转矩阵
def R_z(phi):
    return np.array([
        [np.cos(phi),  np.sin(phi), 0],
        [-np.sin(phi), np.cos(phi), 0],
        [0,           0,          1]
    ])

def R_x(phi):
    return np.array([
        [1, 0,           0],
        [0, np.cos(phi), np.sin(phi)],
        [0, -np.sin(phi), np.cos(phi)]
    ])

# 注意旋转角度为负值
R = R_z(-Omega) @ R_x(-i) @ R_z(-omega)

# 步骤6：应用旋转矩阵转换到GCRS坐标系
position_perifocal = np.array([x_p, y_p, 0])
velocity_perifocal = np.array([v_xp, v_yp, 0])

position_gcrs = R @ position_perifocal
velocity_gcrs = R @ velocity_perifocal

# 输出结果
print(f"卫星在GCRS中的位置 (km): X = {position_gcrs[0]:.6f}, Y = {position_gcrs[1]:.6f}, Z = {position_gcrs[2]:.6f}")
print(f"卫星在GCRS中的速度 (km/s): vx = {velocity_gcrs[0]:.6f}, vy = {velocity_gcrs[1]:.6f}, vz = {velocity_gcrs[2]:.6f}")

# 验证步骤

# 1. 计算总机械能
v = np.linalg.norm(velocity_gcrs)
epsilon = (v**2) / 2 - mu / r
expected_epsilon = -mu / (2 * a)
print(f"总机械能 ε: {epsilon:.6f} km^2/s^2")
print(f"期望的总机械能 ε_expected: {expected_epsilon:.6f} km^2/s^2")

# 2. 计算角动量向量
h_vector = np.cross(position_gcrs, velocity_gcrs)
h_computed = np.linalg.norm(h_vector)
print(f"计算得到的角动量 |h|: {h_computed:.6f} km^2/s")
print(f"给定的角动量 h: {h:.6f} km^2/s")

# 3. 反向计算轨道根数

# 计算半长轴 a 反向验证
a_computed = h_computed**2 / (mu * (1 - e**2))
print(f"反向计算的半长轴 a_computed: {a_computed:.6f} km")

# 计算偏心率 e 反向验证
# e = sqrt(1 + (2*epsilon*h**2) / mu**2)
e_computed = np.sqrt(1 + (2 * epsilon * h_computed**2) / mu**2)
print(f"反向计算的偏心率 e_computed: {e_computed:.12f}")

# 验证角动量一致性
if np.isclose(h_computed, h, atol=1e-6):
    print("角动量一致性验证通过。")
else:
    print("角动量一致性验证失败。")

# 验证机械能一致性
if np.isclose(epsilon, expected_epsilon, atol=1e-6):
    print("机械能一致性验证通过。")
else:
    print("机械能一致性验证失败。")
