import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import gpxpy

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

direc = 'C:/Users/willi/Downloads'
gpxfn = f'{direc}/Morning_Run.gpx'

with open(gpxfn, 'r') as file:
    lines = file.readlines()
hr = []
for ll in lines:
    if 'gpxtpx:hr' in ll:
        hr.append(int(ll.split('>')[1].split('<')[0]))
f = open(gpxfn, 'r')
gpx = gpxpy.parse(f)
pts = gpx.tracks[0].segments[0].points
'''compute distance (input is [lat, long])'''
latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
time_s = np.array([pts[0].time_difference(pt) for pt in pts])  # seconds elapsed between gpx pts
time_min = time_s/60.

plt.plot(time_min, hr)
plt.xlabel('time (min)')
plt.ylabel('HR')
plt.grid()
plt.show()

if __name__ == '__main__':
    pass
