from jplephem.spk import SPK
import numpy as np

# 打开SPK文件
kernel = SPK.open("D://PycharmProjects//huawei_math//doc//附件3-de200.bsp")

# 定义MJD时间点
mjd = 57062.0
# 将MJD转换为儒略日JD
jd = mjd + 2400000.5

# 计算地球质心的位置
position_earth_barycenter = kernel[0, 3].compute(jd)

# 计算地球本身的位置（地心）
position_earth_geocenter = kernel[3, 399].compute(jd)

# 打印结果
print(f"Earth Barycenter Position at MJD {mjd}: {position_earth_barycenter}")
print(f"Earth Geocenter Position at MJD {mjd}: {position_earth_geocenter}")