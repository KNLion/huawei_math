from jplephem.spk import SPK
import numpy as np

kernel = SPK.open("D://PycharmProjects//huawei_math//doc//附件3-de200.bsp")



mjd = 57062.0
jd = np.array([mjd + 2400000.5])

# jd= np.array([2457061.5,2457062.5,2457063.5,2457064.5])
position = kernel[0,3].compute(jd)

print(position)

for segment in kernel.segments:
    print(f"Target: {segment.target}, Center: {segment.center}, Description: {segment.describe()}")