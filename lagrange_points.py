# seeing if I can figure out the 5 lagrange points without looking it up

import matplotlib.pyplot as plt
import numpy as np

# sun at (0,0)
# earth at (1,0)

maxlev = .01
pau = 1.5  # au

g = 6.67408e-11  # m^3/kg/s^2 gravitational constant
msat = 1.  # kg mass of satellite
msun = 1.989e30  # kg mass of sun
# mearth = 5.972e24  # kg mass of earth
mearth = msun/10.
au = 1.496e11  # m
xcm = mearth * au / (mearth + msun)
# rearth = 6.371e6  # m radius of earth
# rsun = 6.96e8  # m radius of sun
rlim = 1.e-4 * au  # au
x, y = np.linspace(- pau * au, pau * au, num=500), np.linspace(-pau * au, pau * au, num=500)
x1d, y1d = x, np.zeros_like(x)
xau, yau = np.linspace(- pau, pau, num=500), np.linspace(-pau, pau, num=500)
xx, yy = np.meshgrid(x, y)


def force(d, m1, m2):
    f = g * m1 * m2 / d ** 2
    f[np.where(d < rlim)] = np.nan
    return f


rsun = np.sqrt(xx ** 2 + yy ** 2)
rearth = np.sqrt((xx - au) ** 2 + yy ** 2)
rcm = np.sqrt((xx - xcm) ** 2 + yy ** 2)
asun = np.arctan2(yy, xx) + np.pi
aearth = np.arctan2(yy, (xx - au)) + np.pi
acm = np.arctan2(yy, (xx - xcm)) + np.pi

fsatsun = force(rsun, msun, msat)  # force of sun on sat
fsatearth = force(rearth, mearth, msat)  # force of earth on sat
fxsatsun, fysatsun = fsatsun * np.cos(asun), fsatsun * np.sin(asun)
fxsatearth, fysatearth = fsatearth * np.cos(aearth), fsatearth * np.sin(aearth)
fsat = np.sqrt((fxsatsun + fxsatearth) ** 2 + (fysatsun + fysatearth) ** 2)
# fearthsun = force(np.array([au]), msun, mearth)  # force of sun on earth

# plt.figure('force on satellite')
# plt.plot([1], [0], 'ko')
# con = plt.contourf(xau, yau, fsat, levels=np.linspace(0, maxlev))  # np.nanmax(fsat)))
# plt.colorbar()

# want same angular velocity w=v/r where r is to cm
wearth = np.sqrt(g * msun / (au - xcm) ** 3)  # rad/s
fsat_wearth = msat * wearth ** 2 * rcm  # force on satellite at radius rcm that gives ang vel of wearth
fxsatsun_wearth, fysatsun_wearth = fsat_wearth * np.cos(acm), fsat_wearth * np.sin(acm)
fnetsat = np.sqrt((fxsatsun + fxsatearth - fxsatsun_wearth) ** 2 + (fysatsun + fysatearth - fysatsun_wearth) ** 2)

plt.figure('satellite net force')
plt.plot([0, xcm / au, 1], [0, 0, 0], 'ko')
con2 = plt.contourf(xau, yau, fsat - fsat_wearth, levels=np.linspace(-maxlev, maxlev))
plt.contour(xau, yau, fsat - fsat_wearth, (0,), colors='k')  # plot 0-contour
plt.colorbar(con2)

plt.show()
