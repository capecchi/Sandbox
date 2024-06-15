import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import gpxpy
import geopy.distance as dist

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

direc = 'C:/Users/willi/Dropbox/running_stuff/routes/'
# fn = f'{direc}5-23-24_run.gpx'
fn = f'{direc}5-15-24_run.gpx'
m_per_mi = 1609.34


def lookat_gpx():
    f = open(fn, 'r')
    fig, (ax, ax2) = plt.subplots(ncols=2)
    gpx = gpxpy.parse(f)
    pts = gpx.tracks[0].segments[0].points
    latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
    dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # m
    # dis *= normto / (sum(dis) / m_per_mi)
    cumdist_mile = np.append(0, np.cumsum(dis / m_per_mi))
    alt = np.array([pt.elevation for pt in pts])
    print(f'{len(latlon[0, :])} pts found in {fn}')
    ax.plot(latlon[1, :], latlon[0, :], 'o-', label=fn)
    # ax.legend()
    ax2.plot(cumdist_mile, alt)
    ax.set_xlabel('lon')
    ax.set_ylabel('lat')
    plt.show()


def compare_gpx():
    fn1, fn2 = f'{direc}Black_Forest_Ultra_100k.gpx', f'{direc}blackforest_race_10-2-22.gpx'
    fig, ax = plt.subplots()
    for fn in [fn1, fn2]:
        f = open(fn, 'r')
        gpx = gpxpy.parse(f)
        pts = gpx.tracks[0].segments[0].points
        latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
        print(f'{len(latlon[0, :])} pts found in {fn}')
        ax.plot(latlon[0, :], latlon[1, :], label=fn)
    ax.legend()


if __name__ == '__main__':
    lookat_gpx()
    # compare_gpx()
