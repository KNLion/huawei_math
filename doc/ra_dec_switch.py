import math

# 赤经和赤纬（度）
ra_deg = 83.63307631324167
dec_deg = 22.014493269173464

# 转换为弧度
ra_rad = math.radians(ra_deg)
dec_rad = math.radians(dec_deg)

# 计算方向向量的x, y, z分量
cos_dec = math.cos(dec_rad)
x = cos_dec * math.cos(ra_rad)
y = cos_dec * math.sin(ra_rad)
z = math.sin(dec_rad)

# 输出方向向量
print(f"Direction vector in BCRS: ({x}, {y}, {z})")
