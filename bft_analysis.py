import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
import gpxpy
import geopy.distance as dist

if os.path.isdir('C:/Users/Owner'):
	direc = 'C:/Users/Owner/PycharmProjects/Sandbox/data/'
elif os.path.isdir('C:/Users/wcapecch'):
	direc = 'C:/Users/wcapecch/PycharmProjects/Sandbox/data/'
else:
	direc = None
	print('directory not found- where are you??')

m_per_mi = 1609.34


def ascent_descent_flat(gpxfn, normto=None):
	m_per_mi = 1609.34
	f = open(gpxfn, 'r')
	gpx = gpxpy.parse(f)
	pts = gpx.tracks[0].segments[0].points
	'''compute distance (input is [lat, long])'''
	latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
	dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # m
	# normalize to recorded distance- not sure why we don't get the same dist garmin recorded
	if normto is not None:
		print(f'data shows {sum(dis) / m_per_mi:.2f}mi, normalizing to {normto} recorded by Garmin')
		dis *= normto / (sum(dis) / m_per_mi)
	cumdist_mile = np.append(0, np.cumsum(dis / m_per_mi))
	alt = np.array([pt.elevation for pt in pts])  # m
	dt = np.array([(pts[i + 1].time - pts[i].time).seconds for i in np.arange(len(pts) - 1)])
	dalt = np.array([alt[i + 1] - alt[i] for i in np.arange(len(alt) - 1)])  # m
	dpath = np.sqrt(dis ** 2 + dalt ** 2)
	pace_flat = dt / dis  # s/m
	pace = dt / dpath  # s/m
	spm_to_minpmil = m_per_mi / 60.
	pace_flat, pace = pace_flat * spm_to_minpmil, pace * spm_to_minpmil
	kernel_size = 50
	kernel = np.ones(kernel_size) / kernel_size
	pace_sm = np.convolve(pace, kernel, mode='same')
	pace_sm[pace_sm > 30] = np.nan  # if slower than 30/mile, remove
	
	ks = 10
	kern = np.ones(ks) / ks
	grade = np.convolve(dalt / dis, kern, mode='same')
	grade_cutoff = .05
	ascent = np.where(grade > grade_cutoff)
	descent = np.where(grade < -grade_cutoff)
	flat = np.where(abs(grade) <= grade_cutoff)
	
	# fig3, axx = plt.subplots()
	# axx.plot(cumdist_mile[1:], grade)
	# plt.show()
	
	prop_cycle = plt.rcParams['axes.prop_cycle']
	clrs = prop_cycle.by_key()['color']
	fig, ax1 = plt.subplots(figsize=(10, 4))
	ax1r = ax1.twinx()
	# ax1.plot(cumdist_mile[1:], pace)
	ax1.plot(cumdist_mile, alt)
	ax1.plot(cumdist_mile[ascent], alt[ascent], 'o', ms=3, c=clrs[0], label='ascent')
	ax1.plot(cumdist_mile[descent], alt[descent], 'o', ms=3, c=clrs[1], label='descent')
	ax1.plot(cumdist_mile[flat], alt[flat], 'o', ms=3, c=clrs[2], label='flat')
	ax1r.plot(cumdist_mile[1:], pace_sm, clrs[3])
	ax1.set_xlabel('dist (mi)')
	ax1.set_ylabel('elev (m)')
	ax1.legend()
	ax1r.set_ylabel('pace (min/mi)')
	ax1r.set_ylim((0, 25))
	plt.tight_layout()
	
	fig2, (axa, axb, axc) = plt.subplots(ncols=3, figsize=(10, 4), sharey='row')
	ava, avb, avc = np.nanmean(pace[ascent] * dpath[ascent]) / np.nanmean(dpath[ascent]), np.nanmean(
		pace[descent] * dpath[descent]) / np.nanmean(dpath[descent]), np.nanmean(pace[flat] * dpath[flat]) / np.nanmean(
		dpath[flat])
	dista, distb, distc = np.sum(dpath[ascent]) / m_per_mi, np.sum(dpath[descent]) / m_per_mi, np.sum(
		dpath[flat]) / m_per_mi
	print(
		f'{ava:.2f} ascent, {avb:.2f} descent, {avc:.2f} flat\n{dista + distb + distc:.2f}mi, {(ava * dista + avb * distb + avc * distc) / 60:.2f}h, {sum(dt) / 60 / sum(dpath) * m_per_mi:.2f}min/mile')
	ascent_pace, descent_pace, flat_pace = np.copy(pace_sm), np.copy(pace_sm), np.copy(pace_sm)
	ascent_pace[:], descent_pace[:], flat_pace[:] = np.nan, np.nan, np.nan
	ascent_pace[ascent] = pace_sm[ascent]
	descent_pace[descent] = pace_sm[descent]
	flat_pace[flat] = pace_sm[flat]
	axa.plot(cumdist_mile[1:], ascent_pace)
	axa.axhline(ava, ls='--', c='k')
	axa.annotate(f'{ava:.2f}- {dista:.2f}mi', (1, ava))
	axb.plot(cumdist_mile[1:], descent_pace)
	axb.axhline(avb, ls='--', c='k')
	axb.annotate(f'{avb:.2f}- {distb:.2f}mi', (1, avb))
	axc.plot(cumdist_mile[1:], flat_pace)
	axc.axhline(avc, ls='--', c='k')
	axc.annotate(f'{avc:.2f}- {distc:.2f}mi', (1, avc))
	axa.set_ylabel('pace (min/mile)')
	axa.set_xlabel('ascent')
	axb.set_xlabel('descent')
	axc.set_xlabel('flat')
	plt.tight_layout()
	
	plt.show()
	a = 1


if __name__ == '__main__':
	fn1 = f'{direc}bft_sec2_6-11-22.gpx'
	fn2 = f'{direc}bft_south_7-16-22.gpx'
	
	for fn, nt in zip([fn1, fn2], [17.47, 23.15]):
		ascent_descent_flat(fn, normto=nt)
