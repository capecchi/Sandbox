import matplotlib.pyplot as plt
import numpy as np
import os
import gpxpy
import geopy.distance as dist
import pandas as pd

clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']
if os.path.isdir('C:/Users/Owner'):
	direc = 'C:/Users/Owner/PycharmProjects/Sandbox/data/'
elif os.path.isdir('C:/Users/wcapecch'):
	direc = 'C:/Users/wcapecch/PycharmProjects/Sandbox/data/'
else:
	direc = None
	print('directory not found- where are you??')

m_per_mi = 1609.34


def lookat_gpx():
	fn = f'{direc}Bear_100.gpx'
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
	ax.plot(latlon[0, :], latlon[1, :], label=fn)
	ax.legend()
	ax2.plot(cumdist_mile, alt)
	plt.show()


def compare_gpx(do=None):
	if do is None:
		do1, do2 = (f'{direc}Zion_2023.gpx', 'course'), (f'{direc}zion_race_4-15-23.gpx', 'race')
	else:
		do1, do2 = do
	fig, ax = plt.subplots()
	fig2, ax2 = plt.subplots()
	for do in [do1, do2]:
		fn, lbl = do[0], do[1]
		f = open(fn, 'r')
		gpx = gpxpy.parse(f)
		pts = gpx.tracks[0].segments[0].points
		latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
		alt = np.array([pt.elevation for pt in pts])
		dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # m
		cumdist_mile = np.append(0, np.cumsum(dis / m_per_mi))
		cumdist_mile /= max(cumdist_mile)  # normalize to 1 for direct comparison of gpx
		print(f'{len(latlon[0, :])} pts found in {fn}')
		ax.plot(latlon[1, :], latlon[0, :], label=lbl)
		ax2.plot(cumdist_mile, alt, label=lbl)
	ax.legend()
	ax2.legend()
	plt.show()


def analyze_worlds_end_efforts():
	csv_fn = f'{direc}worlds_end_data.csv'
	df = pd.read_csv(csv_fn)
	dist = [float(d[:-2]) for d in df['dist'].values]  # take 'mi' off end of dist column
	pace = [p[:-3] for p in df['pace'].values]  # take off '/mi' off end of pace column
	eff_pace = [p[:-3] for p in df['effort pace'].values]
	pace = [float(p[:2]) + float(p[-3:-1]) / 60 for p in pace]  # convert 'mm\'ss"' to float minutes
	eff_pace = [float(p[:2]) + float(p[-3:-1]) / 60 for p in eff_pace]
	elev = [float(e[:-2]) for e in df['elev'].values]  # remove 'ft'
	desc = [float(d[:-2]) for d in df['descent'].values]  # remove 'ft'
	cd = np.cumsum(dist)
	
	pace_pn = [1 if pace[i + 1] > pace[i] else -1 for i in range(len(pace) - 1)]
	effp_pn = [1 if eff_pace[i + 1] > eff_pace[i] else -1 for i in range(len(pace) - 1)]
	
	fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)
	ax1.plot(cd, pace, 'o-', label='pace')
	ax1.plot(cd, eff_pace, 'o-', label='effort pace')
	w = 0.4
	ax2.bar(cd - w / 2, elev, width=w, label='elevation gain')
	ax2.bar(cd + w / 2, desc, width=w, label='descent')
	ax3.bar(cd[1:] - w / 2, pace_pn, width=w, label='pace')
	ax3.bar(cd[1:] + w / 2, effp_pn, width=w, label='effort pace')
	
	ax1.legend()
	ax2.legend()
	ax3.legend()
	ax1.set_ylabel('pace (min/mi)')
	ax2.set_ylabel('ft')
	ax3.set_xlabel('dist (mi)')
	ax3.set_ylabel('pace change direction')
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	# analyze_worlds_end_efforts()
	
	doit = ((f'{direc}worlds_end_official.gpx', 'course'), (f'{direc}worlds_end_race_6-1-24.gpx', 'race'))
	compare_gpx(do=doit)
