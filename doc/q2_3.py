from jplephem.spk import SPK
import numpy as np

# 常数
C = 299792.458  # 光速，km/s
DEG_TO_RAD = np.pi / 180.0
MILLI_ARCSEC_TO_DEG = 1.0 / 3600000.0


# 步骤1：读取脉冲星RA、Dec及自行参数
def get_pulsar_direction(mjd, ra_deg, dec_deg, dt_ra_mas_per_year, dt_dec_mas_per_year, pch_pm):
    # 计算时间差（年）
    delta_days = mjd - pch_pm
    delta_years = delta_days / 365.25  # 大约

    # 计算RA和Dec的自行调整（毫角秒 -> 度）
    delta_ra_deg = dt_ra_mas_per_year * delta_years * MILLI_ARCSEC_TO_DEG / 1000.0
    delta_dec_deg = dt_dec_mas_per_year * delta_years * MILLI_ARCSEC_TO_DEG / 1000.0

    # 更新RA和Dec
    ra_updated = ra_deg + delta_ra_deg
    dec_updated = dec_deg + delta_dec_deg

    # 转换为弧度
    ra_rad = ra_updated * DEG_TO_RAD
    dec_rad = dec_updated * DEG_TO_RAD

    # 计算单位向量
    n = np.array([
        np.cos(dec_rad) * np.cos(ra_rad),
        np.cos(dec_rad) * np.sin(ra_rad),
        np.sin(dec_rad)
    ])

    return n


# 步骤2：读取DE200历表，获取地球-月亮质心在SSB坐标系中的位置
def get_earth_moon_barycenter_position(kernel, mjd):
    jd = np.array([mjd + 2400000.5])
    earth_moon_barycenter = kernel[0, 3].compute(jd)  # Target=3为Earth-Moon Barycenter
    return earth_moon_barycenter.flatten()  # 转换为一维数组


# 步骤3：获取地球质心相对于地球-月亮质心的位移
def get_earth_geocenter_relative_position(kernel, mjd):
    jd = np.array([mjd + 2400000.5])
    earth_geocenter_rel = kernel[3, 399].compute(jd)  # Target=399为Earth Geocenter relative to Earth-Moon Barycenter
    return earth_geocenter_rel.flatten()  # 转换为一维数组


# 步骤4：获取卫星在GCRS中的位置（从问题1获取）
def get_satellite_gcrs_position():
    # 这里需要替换为问题1实际计算得到的卫星位置
    # 示例值：
    """卫星在GCRS中的位置 (km): X = 1274.913415, Y = -1848.851965, Z = 6507.262655
卫星在GCRS中的速度 (km/s): vx = -6.210795, vy = 3.746127, vz = 2.276331"""
    return np.array([1274.913415, -1848.851965, 6507.262655])  # 单位：km


# 步骤5：转换卫星位置到SSB坐标系
def convert_gcrs_to_ssb(earth_moon_barycenter_ssb, earth_geocenter_rel, satellite_gcrs):
    earth_geocenter_ssb = earth_moon_barycenter_ssb + earth_geocenter_rel
    satellite_ssb = earth_geocenter_ssb + satellite_gcrs
    return satellite_ssb


# 步骤6：计算传播路径时间差
def compute_time_delay(satellite_ssb, pulsar_direction):
    # 点积
    projection = np.dot(satellite_ssb, pulsar_direction)
    delta_t = projection / C  # 单位：秒
    return delta_t


def main():
    # 文件路径（根据实际路径调整）
    de200_path = "D://PycharmProjects//huawei_math//doc//附件3-de200.bsp"

    # 给定的MJD
    mjd = 57062.0

    # 读取附件1和附件4的数据
    # 假设附件1和附件4的内容如下（根据实际文件内容调整）
    # 这里直接硬编码为示例值
    ra_deg = 83.63307631324167  # 赤经，单位：度
    dec_deg = 22.014493269173464  # 赤纬，单位：度
    dt_ra_mas_per_year = -14.7  # 毫角秒/年
    dt_dec_mas_per_year = 2.0  # 毫角秒/年
    pch_pm = 57715.000000295  # 参考历元，MJD

    # 获取脉冲星方向向量
    pulsar_n = get_pulsar_direction(mjd, ra_deg, dec_deg, dt_ra_mas_per_year, dt_dec_mas_per_year, pch_pm)
    print("脉冲星方向单位向量 n:", pulsar_n)

    # 打开DE200历表文件
    kernel = SPK.open(de200_path)

    # 获取地球-月亮质心在SSB坐标系中的位置
    earth_moon_barycenter_ssb = get_earth_moon_barycenter_position(kernel, mjd)
    print("地球-月亮质心在SSB坐标系中的位置 (km):", earth_moon_barycenter_ssb)

    # 获取地球质心相对于地球-月亮质心的位移
    earth_geocenter_rel = get_earth_geocenter_relative_position(kernel, mjd)
    print("地球质心相对于地球-月亮质心的位移 (km):", earth_geocenter_rel)

    # 获取卫星在GCRS中的位置
    satellite_gcrs = get_satellite_gcrs_position()
    print("卫星在GCRS中的位置 (km):", satellite_gcrs)

    # 转换卫星位置到SSB坐标系
    satellite_ssb = convert_gcrs_to_ssb(earth_moon_barycenter_ssb, earth_geocenter_rel, satellite_gcrs)
    print("卫星在SSB坐标系中的位置 (km):", satellite_ssb)

    # 计算传播路径时间差
    delta_t = compute_time_delay(satellite_ssb, pulsar_n)
    print("传播路径时间差 Δt (秒):", delta_t)

    # 关闭历表文件
    kernel.close()


if __name__ == "__main__":
    main()
