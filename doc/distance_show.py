import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.rcParams['font.family'] = 'Microsoft YaHei'

# 提供的数据
earth_moon_barycenter_position_ssb = np.array([-1.12094190e+08, 8.75121480e+07, 3.79151058e+07])
satellite_position_gcrs = np.array([1274.913415, -1848.851965, 6507.262655])
satellite_position_ssb = np.array([-1.12088170e+08, 8.75114135e+07, 3.79220678e+07])

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制地球-月亮质心在SSB坐标系中的位置
ax.scatter(earth_moon_barycenter_position_ssb[0], earth_moon_barycenter_position_ssb[1], earth_moon_barycenter_position_ssb[2], color='blue', label='地球-月亮质心在SSB坐标系中的位置')

# 绘制卫星在GCRS中的位置
ax.scatter(satellite_position_gcrs[0], satellite_position_gcrs[1], satellite_position_gcrs[2], color='red', label='卫星在GCRS中的位置')

# 绘制卫星在SSB坐标系中的位置
ax.scatter(satellite_position_ssb[0], satellite_position_ssb[1], satellite_position_ssb[2], color='green', label='卫星在SSB坐标系中的位置')

# 设置坐标轴标签
ax.set_xlabel('X 轴 (km)')
ax.set_ylabel('Y 轴 (km)')
ax.set_zlabel('Z 轴 (km)')

# 显示图例
ax.legend()

# 显示图形
plt.show()
