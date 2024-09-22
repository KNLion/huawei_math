from jplephem.spk import SPK
import numpy as np

# 常数
C = 299792.458  # 光速，km/s


# 步骤1：读取DE200历表，获取地球质心在SSB坐标系中的位置
def get_earth_geocenter_position(de200_path, mjd):
    kernel = SPK.open(de200_path)
    jd = np.array([mjd + 2400000.5])
    earth_geocenter_position = kernel[0, 399].compute(jd)  # Target=399为Earth Geocenter
    return earth_geocenter_position.flatten()  # 转换为一维数组


# 步骤2：获取卫星在GCRS中的位置（从问题1获取）
def get_satellite_gcrs_position():
    # 这里需要替换为问题1实际计算得到的卫星位置
    # 示例值：
    return np.array([1274.913415, -1848.851965, 6507.262655])  # 单位：km

""" 第一问的答案:X = 1274.913415, Y = -1848.851965, Z = 6507.262655"""

# 步骤3：转换卫星位置到SSB坐标系
def convert_gcrs_to_ssb(earth_geocenter_ssb, satellite_gcrs):
    return earth_geocenter_ssb + satellite_gcrs


# 步骤4：计算卫星相对于SSB的距离
def compute_distance(position_ssb):
    return np.linalg.norm(position_ssb)


# 步骤5：计算传播路径时间差
def compute_time_delay(distance_km):
    return distance_km / C  # 单位：秒


def main():
    # 文件路径（根据实际路径调整）
    de200_path = "D://PycharmProjects//huawei_math//doc//附件3-de200.bsp"

    # 给定的MJD
    mjd = 57062.0

    # 获取地球质心在SSB坐标系中的位置
    earth_geocenter_ssb = get_earth_geocenter_position(de200_path, mjd)
    print("地球质心在SSB坐标系中的位置 (km):", earth_geocenter_ssb)

    # 获取卫星在GCRS中的位置
    satellite_gcrs = get_satellite_gcrs_position()
    print("卫星在GCRS中的位置 (km):", satellite_gcrs)

    # 转换卫星位置到SSB坐标系
    satellite_ssb = convert_gcrs_to_ssb(earth_geocenter_ssb, satellite_gcrs)
    print("卫星在SSB坐标系中的位置 (km):", satellite_ssb)

    # 计算距离
    distance = compute_distance(satellite_ssb)
    print("卫星相对于SSB的距离 (km):", distance)

    # 计算传播路径时间差
    delta_t = compute_time_delay(distance)
    print("传播路径时间差 Δt (秒):", delta_t)


if __name__ == "__main__":
    main()
