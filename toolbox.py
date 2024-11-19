import matplotlib.pyplot as plt
import numpy as np
import gpxpy
import geopy.distance as dist

clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']


def fix_gps():
	file = 'C:/Users/wcapecch/Downloads/Bad_gps_.gpx'
	f = open(file, 'r')
	gpx = gpxpy.parse(f)
	pts = gpx.tracks[0].segments[0].points
	latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
	dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # [m]
	cumdist = np.append(0, np.cumsum(dis))
	fig, (ax1, ax2) = plt.subplots(nrows=2, sharex='col')
	ax1.plot(cumdist, latlon[0, :], 'o-')
	ax2.plot(cumdist, latlon[1, :], 'o-')
	ax1.set_ylabel('lat')
	ax2.set_ylabel('lon')
	ax2.set_xlabel('cum dist [m]')
	plt.show()


if __name__ == '__main__':
	pass