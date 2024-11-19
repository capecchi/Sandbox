import os

import fitparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import gpxpy
import geopy.distance as dist  # takes (lat, lon) as input coords

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']


def extract_coords_gpx(runfile, return_ts=False):
    # returns [lon, lat, elev, dcum, dstep, tcum, tstep]
    lat, lon = 100., 0.  # impossible set of coords to start with
    print(f'extracting gpx data from {runfile}')
    with open(runfile, 'r') as f:
        gpx = gpxpy.parse(f)
        activity_timestamp = gpx.time
        run_coords, ts = [], []
        for track in gpx.tracks:
            for segment in track.segments:
                for i, point in enumerate(segment.points):
                    ts.append(point.time.replace(tzinfo=None))
                    lat, lon, elev = point.latitude, point.longitude, point.elevation
                    tcum = point.time_difference(segment.points[0])  # time since first point
                    if i == 0:
                        dx, dt = 0, 0
                    else:
                        if segment.points[i - 1].time_difference(segment.points[i]) != 1:
                            a = 1
                        prev = segment.points[i - 1]
                        dx = dist.distance((lat, lon), (prev.latitude, prev.longitude)).m
                        dt = point.time_difference(segment.points[i - 1])  # time since last point
                    run_coords.append([lon, lat, elev, dx, dx, tcum, dt])
    coords = np.array(run_coords)
    coords[:, 3] = np.cumsum(coords[:, 3])  # convert dx to cumulative distance [m]

    if return_ts:
        return coords, ts, activity_timestamp
    else:
        return coords, activity_timestamp


def extract_coords_fit(runfile, return_ts=False):  # [lon, lat, elev, dcum, dstep, tcum, tstep]
    # note divide by 11930465. below is to convert 32-bit integer to get value in decimal degrees
    # 11930465 = 2^32/360

    print(f'extracting fit data from {runfile}')
    coords = []
    ts, lat, lon, dist = [], [], [], []
    ff = fitparse.FitFile(runfile)
    for rec in ff.get_messages():
        if rec.get_value('activity_type') == 'running':
            if rec.get_value('position_lat') is not None:
                ts.append(rec.get_value('timestamp'))
                lat.append(rec.get_value('position_lat') / 11930465.)
                lon.append(rec.get_value('position_long') / 11930465.)
                dist.append(rec.get_value('distance'))  # [m]
    for i in np.arange(len(ts)):
        if i == 0:
            coords.append([lon[i], lat[i], None, dist[i], 0., 0., 0.])
        else:
            tcum = (ts[i] - ts[0]).days * 3600. * 24 + (ts[i] - ts[0]).seconds
            coords.append([lon[i], lat[i], None, dist[i], dist[i] - dist[i - 1], tcum, (ts[i] - ts[i - 1]).seconds])
    # coords.insert([lon[0], lat[0], None, dist[0], 0., 0., 0.])
    if return_ts:
        return np.array(coords), ts
    else:
        return np.array(coords)


def compare_fit_gpx():
    fit1 = 'data/vis_check/teanaway_coros.fit'
    cfit, tsfit = extract_coords_fit(fit1, return_ts=True)
    gpx1 = 'data/vis_check/teanaway_coros.gpx'  # file exported from coros app- NOT ok!
    cgpx, tsgpx, activity_time = extract_coords_gpx(gpx1, return_ts=True)

    # [lon, lat, elev, dcum, dstep, tcum, tstep]
    plt.figure()  # plot out lat/lon for both extractions
    plt.plot(cfit[:, 0], cfit[:, 1], label='fit')
    plt.plot(cgpx[:, 0], cgpx[:, 1], label='gpx')
    plt.legend()

    plt.figure()  # plotting longitude vs cumulative time since fit has no elevation data
    plt.plot(cfit[:, 5], cfit[:, 0], label='fit')
    plt.plot(cgpx[:, 5], cgpx[:, 0], label='gpx')
    plt.legend()


def plot_activity_timesteps(files=None, labels=None):
    plt.figure()
    if labels is None:
        lbls = [f.split('/')[-1] for f in files]  # drop off direc
    for i in range(len(files)):
        coords, activity_time = extract_coords_gpx(files[i])
        xx = np.linspace(0, 1, num=len(coords[1:, 5]))
        dt = coords[1:, 5] - coords[:-1, 5]
        if min(dt) < 0:
            ibad = np.where(dt < 0)[0][0] + 1  # first index of bad time point
            print(f'bad coords of {files[i]}: {coords[ibad,:2]}')
            posdt, negdt = np.copy(dt), np.copy(dt)
            posdt[np.where(dt < 0)] = np.nan
            negdt[np.where(dt > 0)] = np.nan
            plt.plot(xx, np.log(posdt), 'o', label=f'{activity_time.strftime("%Y-%m-%d")} : {lbls[i]}', c=clrs[i])
            plt.plot(xx, -np.log(-negdt), 'o', c=clrs[i])
        else:
            print(f'no timing issue with {files[i]}')

    plt.legend()
    plt.title('dt = time between consecutive data points')
    plt.ylabel('log(dt) [s]')
    # plt.ylabel('longitude [deg]')


if __name__ == '__main__':
    direc = 'data/vis_check/'
    files = [f'{direc}teanaway_coros.gpx', f'{direc}teanaway_coros_support.gpx',
             f'{direc}teanaway_strava.gpx', f'{direc}teanaway_app2.gpx']
    lbls = ['coros app', 'coros support', 'strava', 'coros app 2']

    direc = 'data/new_download/'
    files = [f'{direc}{f}' for f in os.listdir(direc)]
    plot_activity_timesteps(files=files)
    plt.show()
