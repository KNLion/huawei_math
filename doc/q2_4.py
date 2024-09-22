from jplephem.spk import SPK
import numpy as np

# 常数
C = 299792.458  # 光速，km/s
DEG_TO_RAD = np.pi / 180.0  # 度转弧度


# 步骤1：读取DE200历表，获取地球质心在SSB坐标系中的位置
def get_earth_barycenter_position(kernel, mjd):
    jd = np.array([mjd + 2400000.5])
    earth_barycenter_ssb = kernel[0, 3].compute(jd)  # Target=3为Earth Barycenter
    return earth_barycenter_ssb.flatten()  # 转换为一维数组


# 步骤2：获取卫星在GCRS中的位置（从问题1获取）
def get_satellite_gcrs_position():
    # 这里需要替换为问题1实际计算得到的卫星位置
    # 示例值：
    return np.array([1274.913415, -1848.851965, 6507.262655])  # 单位：km


# 步骤3：转换卫星位置到SSB坐标系
def convert_gcrs_to_ssb(kernel, mjd, satellite_gcrs):
    # 获取地球质心在SSB坐标系中的位置
    earth_barycenter_ssb = get_earth_barycenter_position(kernel, mjd)

    # 获取地球质心相对于Earth Barycenter的位移
    jd = np.array([mjd + 2400000.5])
    earth_geocenter_rel = kernel[3, 399].compute(
        jd).flatten()  # Target=399为Earth Geocenter relative to Earth Barycenter

    # 卫星在SSB坐标系中的位置
    satellite_ssb = earth_barycenter_ssb + earth_geocenter_rel + satellite_gcrs
    return satellite_ssb


# 步骤4：计算脉冲星方向向量
def compute_pulsar_direction(attachement1, attachment4, mjd):
    # 从附件1中读取初始RA和Dec（单位：度）
    ra_initial_deg = 83.63307631324167  # 从附件1
    dec_initial_deg = 22.014493269173464  # 从附件1

    # 从附件4中读取参考历元和自行（单位：毫角秒/年）
    pch_pm = 57715.000000295  # 参考历元，单位：MJD
    dt_ra_mas_per_year = -14.7  # 毫角秒/年
    dt_dec_mas_per_year = 2.0  # 毫角秒/年

    # 计算时间差（单位：年）
    delta_days = mjd - pch_pm
    delta_years = delta_days / 365.25  # 近似

    # 计算RA和Dec的变化量（单位：度）
    delta_ra_deg = (dt_ra_mas_per_year * delta_years) / (3600 * 1000)  # 转换为度
    delta_dec_deg = (dt_dec_mas_per_year * delta_years) / (3600 * 1000)  # 转换为度

    # 调整后的RA和Dec（单位：度）
    ra_new_deg = ra_initial_deg + delta_ra_deg
    dec_new_deg = dec_initial_deg + delta_dec_deg

    # 转换为弧度
    ra_new_rad = ra_new_deg * DEG_TO_RAD
    dec_new_rad = dec_new_deg * DEG_TO_RAD

    # 计算单位方向向量
    u_pulsar = np.array([
        np.cos(dec_new_rad) * np.cos(ra_new_rad),
        np.cos(dec_new_rad) * np.sin(ra_new_rad),
        np.sin(dec_new_rad)
    ])

    return u_pulsar


# 步骤5：计算传播路径时间差
def compute_time_delay(r_sat_ssb, u_pulsar):
    delta_t = np.dot(r_sat_ssb, u_pulsar) / C  # 单位：秒
    return delta_t


def main():
    # 文件路径（根据实际路径调整）
    de200_path = "D://PycharmProjects//huawei_math//doc//附件3-de200.bsp"

    # 给定的MJD
    mjd = 57062.0

    # 打开DE200历表文件
    kernel = SPK.open(de200_path)

    # 获取卫星在GCRS中的位置
    satellite_gcrs = get_satellite_gcrs_position()
    print("卫星在GCRS中的位置 (km):", satellite_gcrs)

    # 转换卫星位置到SSB坐标系
    satellite_ssb = convert_gcrs_to_ssb(kernel, mjd, satellite_gcrs)
    print("卫星在SSB坐标系中的位置 (km):", satellite_ssb)

    # 计算脉冲星方向向量
    u_pulsar = compute_pulsar_direction(
        attachement1=None,  # 这里可以扩展为从文件读取
        attachment4=None,  # 这里可以扩展为从文件读取
        mjd=mjd
    )
    print("脉冲星单位方向向量:", u_pulsar)

    # 计算传播路径时间差
    delta_t = compute_time_delay(satellite_ssb, u_pulsar)
    print("传播路径时间差 Δt (秒):", delta_t)

    # 关闭历表文件
    kernel.close()


if __name__ == "__main__":
    main()
