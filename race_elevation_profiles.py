import os
import numpy as np
import matplotlib.pyplot as plt
import gpxpy
import geopy.distance as dist
from helpful_stuff.tools import get_my_direc
import matplotlib

matplotlib.use('TkAgg')  # allows plotting in debug mode

# direc = get_my_direc(append='PycharmProjects/Sandbox/data/', err='cannot locate gpx directory')
direc = 'C:/Users/willi/PycharmProjects/Sandbox/data/'
k50 = f'{direc}superior_race_5-19-18.gpx'
k100 = f'{direc}blackforest_race_10-2-22.gpx'
m100 = f'{direc}Zion_2023.gpx'
teanaway = f'{direc}teanaway_100.gpx'
m_per_mi = 1609.34


def the_version(overlay_teanaway=False):
    nnum = 750
    axes_ratio = .013  # [m/mile]
    x = np.linspace(0, 100, num=nnum, endpoint=True)
    fig1, ax1 = plt.subplots()  # figsize=[14.5, 2])
    ax1.set_aspect(axes_ratio)
    if overlay_teanaway:
        races = (
        (k50, -300, 35, 'k'), (k100, 750, 60, 'k'), (m100, 0, 50, 'k'), (teanaway, 350, 0, 'r'))  # (race, y0, x0)
    else:
        races = ((k50, -300, 35, 'k'), (k100, 750, 60, 'k'), (m100, 0, 50, 'k'))  # (race, y0, x0)
    for (file, y0, x0, c) in races:
        f = open(file, 'r')
        gpx = gpxpy.parse(f)
        pts = gpx.tracks[0].segments[0].points
        latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
        dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # m
        cumdist_mile = np.append(0, np.cumsum(dis / m_per_mi))
        alt = np.array([pt.elevation for pt in pts])
        # make start/end same elevation
        alt += cumdist_mile / cumdist_mile[-1] * (alt[0] - alt[-1]) - alt[0]  # set alt[0]=0
        xp = (cumdist_mile + x0) % 100
        yp = alt - np.average(alt) + y0
        isort = np.argsort(xp)
        xp, yp = xp[isort], yp[isort]
        y = np.interp(x, xp, yp)
        # ax1.plot(xp, yp, 'k')
        ax1.plot(x, y, c=c)
    plt.show()


def not_the_version():
    # single line only, no messaging
    fig1, ax1 = plt.subplots(figsize=[14.5, 2])
    fig2, ax2 = plt.subplots(figsize=[14.5, 2])
    gap, spacing, nnum = .01, 50, 750
    x = np.linspace(0, 1, num=nnum, endpoint=True)
    iends = int(nnum / 10)  # number of points to plot before/after
    last = np.zeros_like(x)
    # long = [('superior50k2018', k50), ('stonemill50M2020', m50), ('blackforest100k2022', k100)]
    long = [('stonemill50M2020', m50), ('superior50k2018', k50), ('blackforest100k2022', k100), ('zion100m2023', m100)]
    short = [('MN50k18', k50), ('MD50M20', m50), ('PA100k22', k100)]
    long = [long[1], long[2], long[3]]
    normto = 1 - gap
    for i, (lbl, file) in enumerate(long):
        f = open(file, 'r')
        gpx = gpxpy.parse(f)
        pts = gpx.tracks[0].segments[0].points
        latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
        dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # m
        # normalize to recorded distance- not sure why we don't get the same dist garmin recorded
        # print(f'data shows {sum(dis) / m_per_mi:.2f}mi, normalizing to {normto} recorded by Garmin')
        dis *= normto / (sum(dis) / m_per_mi)
        cumdist_mile = np.append(0, np.cumsum(dis / m_per_mi))
        alt = np.array([pt.elevation for pt in pts])
        # xalt = np.linspace(0, 1 - gap, num=len(alt), endpoint=True)
        xalt = cumdist_mile
        alt0 = alt - min(alt)  # set so min is at zero, shift up by offset later
        y = np.interp(x, xalt, alt0)
        y[x > max(xalt)] = np.nan
        minbetween = [min(np.roll(y, i) - last) for i in np.arange(len(y))]
        offset = max(minbetween)
        iroll = np.where(minbetween == offset)[0][0]
        ax2.plot(x, y - offset, 'k')  # plot without roll
        y = np.roll(y, iroll) - offset
        xx = np.append(x[-iends:] - 1, np.append(x, x[:iends] + 1))
        yy = np.append(y[-iends:], np.append(y, y[:iends]))
        ax1.plot(xx, yy, 'k')
        xstrt, xend = x[iroll - 1], (xalt[-1] + x[iroll - 1]) % 1
        ystrt, yend = alt0[0] - offset, alt0[-1] - offset
        # ax1.plot([xstrt, xstrt - 1, xstrt + 1, xend, xend - 1, xend + 1], [ystrt, ystrt, ystrt, yend, yend, yend], 'ko',
        #          ms=3)
        last = y + spacing
        if i == 0:
            ax1.plot([0, 1], [-spacing, -spacing], 'b^', ms=5)
        if i == len(long) - 1:
            ax1.plot([0, 1], [max(y) + spacing, max(y) + spacing], 'bv', ms=5)

    ax1.axis('off')
    ax1.set_xlim((-.1, 1.1))
    for ax in [ax1, ax2]:
        plt.sca(ax)
        plt.tight_layout()


if __name__ == '__main__':
    # not_the_version()
    the_version()
    # lookat_gpx()
    # compare_gpx()
    plt.show()
