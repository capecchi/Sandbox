import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import gpxpy
import geopy.distance as dist

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

direc = 'C:/Users/willi/PycharmProjects/Sandbox/data'
gpxfn = 'SHT100_2025.gpx'
f = open(f'{direc}/{gpxfn}', 'r')
m_per_mi = 1609.34

with open(f'{direc}/{gpxfn}', 'r') as file:
    lines = file.readlines()
    hr = []
    for ll in lines:
        if 'gpxtpx:hr' in ll:
            hr.append(int(ll.split('>')[1].split('<')[0]))
gpx = gpxpy.parse(f)
pts = gpx.tracks[0].segments[0].points
latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # m
# dis *= normto / (sum(dis) / m_per_mi)
cumdist_mile = np.append(0, np.cumsum(dis / m_per_mi))
alt = np.array([pt.elevation for pt in pts])
time_s = np.array([pts[0].time_difference(pt) for pt in pts])  # seconds elapsed between gpx pts
time_min = time_s / 60.
time_hr = time_min / 60.
print(f'{len(latlon[0, :])} pts found in {gpxfn}')

# per mile analysis
miles = np.append(np.arange(int(np.ceil(max(cumdist_mile)))), max(cumdist_mile))  # 1-103.7
time_interp = np.interp(miles, cumdist_mile, time_min)
pace = np.diff(time_interp)
hr_mileavg = np.zeros_like(pace)
for i in range(len(miles)-1):
    hr_mileavg[i] = np.mean(hr[np.where((cumdist_mile < miles[i+1]) & (cumdist_mile >= miles[i]))[0]])

fig, (ax, ax2) = plt.subplots(ncols=2)
ax.plot(latlon[0, :], latlon[1, :], label=gpxfn)
ax.legend()
# ax2.plot(cumdist_mile, alt)
ax2.plot(time_hr, cumdist_mile)
plt.show()

# with open(gpxfn, 'r') as file:
#     lines = file.readlines()
# hr = []
# for ll in lines:
#     if 'gpxtpx:hr' in ll:
#         hr.append(int(ll.split('>')[1].split('<')[0]))
# f = open(gpxfn, 'r')
# gpx = gpxpy.parse(f)
# pts = gpx.tracks[0].segments[0].points
# '''compute distance (input is [lat, long])'''
# latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
# time_s = np.array([pts[0].time_difference(pt) for pt in pts])  # seconds elapsed between gpx pts
# time_min = time_s/60.
#
# plt.plot(time_min, hr)
# plt.xlabel('time (min)')
# plt.ylabel('HR')
# plt.grid()
# plt.show()
if __name__ == '__main__':
    pass
