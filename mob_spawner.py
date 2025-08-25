import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

m1 = [-37, 40, 90]
m2 = [-35, 41, 63]

x1 = np.arange(m1[0] - 16, m1[0] + 17)
y1 = np.arange(m1[1] - 16, m1[1] + 17)
z1 = np.arange(m1[2] - 16, m1[2] + 17)

good = []


def radius_3d(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2 + (pt1[2] - pt2[2]) ** 2)


for y in y1:
    for x in x1:
        for z in z1:
            if radius_3d([x, y, z], m1) <= 16 and radius_3d([x, y, z], m2) <= 16:
                good.append([x, y, z])
                print(f'{[x, y, z]}')
a = 1

if __name__ == '__main__':
    pass
