import gpxpy
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import os

if os.path.isdir('C:/Users/Owner'):
	direc = 'C:/Users/Owner/PycharmProjects/Sandbox/data/'
elif os.path.isdir('C:/Users/wcapecch'):
	direc = 'C:/Users/wcapecch/PycharmProjects/Sandbox/data/'
else:
	direc = None
	print('directory not found- where are you??')

k50 = direc + 'superior_spring_50k.gpx'
m50 = direc + 'stone_mill_50M.gpx'
k100 = direc + 'Black_Forest_Ultra_100k.gpx'


def original():
	shadow = 0
	linestyle = 1
	
	fig = plt.figure(figsize=[14.5, 2])
	plt.axis('off')
	plt.tight_layout()
	offset = 0
	x = np.linspace(0, 1, num=500, endpoint=True)
	last = np.zeros_like(x)
	norm = True
	long = [('superior50k2018', k50), ('stonemill50M2020', m50), ('blackforest100k2022', k100)]
	short = [('MN50k18', k50), ('MD50M20', m50), ('PA100k22', k100)]
	for i, (lbl, file) in enumerate(long):
		f = open(file, 'r')
		gpx = gpxpy.parse(f)
		pts = gpx.tracks[0].segments[0].points
		alt = np.array([pt.elevation for pt in pts])
		print(f'{lbl}: {max(alt) - min(alt)}')
		alt0 = alt - min(alt)  # set so min is at zero, shift up by offset later
		alt_norm = alt0 / (max(alt0) - min(alt0))
		xx = np.linspace(0, 1, num=len(alt_norm), endpoint=True)
		if norm:
			y = np.interp(x, xx, alt_norm)
			cross_height, spacing, shadowheight = .1, .1, .1
		else:
			y = np.interp(x, xx, alt0)
			cross_height, spacing, shadowheight = 25, 25, 25
		
		# bnry = bin(int.from_bytes(lbl.encode(), 'big'))[2:]  # makes no sense, uninterpretable
		o = [ord(l) - 97 if ord(l) >= 97 else int(l) for l in
		     lbl.lower()]  # make lowercase then make a=0,b=1,... mapping leaving numbers as numbers
		bnry = ''.join([bin(l)[2:].zfill(5) for l in o])  # give each char 5 digits and convert to binary
		print(lbl + ': ' + bnry)
		nn = np.linspace(0, 1,
		                 num=len(bnry) + 1)  # +1 to make n gaps, another +1 to make an extra gap representing 1 bit
		off = y * 0.
		for j in np.arange(len(bnry)):
			off[(nn[j] <= x) & (x <= nn[j + 1])] = int(bnry[j])
		y1 = np.copy(y)
		y1[off == 0] = np.nan
		offset = min(last - y) - spacing - cross_height
		
		if shadow:
			plt.plot(x, y + offset, '#6b8e23')
			plt.fill_between(x, y1 + offset - shadowheight, y1 + offset, facecolor='k')  # facecolor='0.8')
		# plt.plot(x, y1 + offset, '#6b8e23', path_effects=[pe.SimpleLineShadow(offset=(0, -4)), pe.Normal()], linewidth=2)
		# offset = min(y) - offset - .7
		if linestyle:
			plt.plot(x, y + offset, '#6b8e23')
			plt.plot(x, y1 + offset - cross_height, '#6b8e23')
		# plt.plot(x, y + offset, '#6b8e23', linestyle=':')
		# plt.plot(x, y1 + offset, '#6b8e23')
		
		last = y + offset
		plt.plot([nn[1], nn[1]], [np.interp(nn[1], x, y) + offset - cross_height,
		                          np.interp(nn[1], x, y) + offset + cross_height], '#6b8e23')


def minimize_offset():
	fig = plt.figure(figsize=[14.5, 2])
	plt.axis('off')
	plt.tight_layout()
	offset = 0
	x = np.linspace(0, 1, num=500, endpoint=True)
	last = np.zeros_like(x)
	long = [('superior50k2018', k50), ('stonemill50M2020', m50), ('blackforest100k2022', k100)]
	short = [('MN50k18', k50), ('MD50M20', m50), ('PA100k22', k100)]
	for i, (lbl, file) in enumerate(long):
		o = [ord(l) - 97 if ord(l) >= 97 else int(l) for l in
		     lbl.lower()]  # make lowercase then make a=0,b=1,... mapping leaving numbers as numbers
		bnry = ''.join([bin(l)[2:].zfill(5) for l in o])  # give each char 5 digits and convert to binary
		print(lbl + ': ' + bnry)
		nn = np.linspace(0, 1,
		                 num=len(bnry) + 1 + 1)  # +1 to make n gaps, another +1 to make an extra gap representing 1 bit
		
		f = open(file, 'r')
		gpx = gpxpy.parse(f)
		pts = gpx.tracks[0].segments[0].points
		alt = np.array([pt.elevation for pt in pts])
		print(f'{lbl}: {max(alt) - min(alt)}')
		alt0 = alt - min(alt)  # set so min is at zero, shift up by offset later
		alt_norm = alt0 / (max(alt0) - min(alt0))
		xx = np.linspace(0, nn[-2], num=len(alt_norm), endpoint=True)  # leave gap at end, map to nn[-2]
		y = np.interp(x, xx, alt_norm)
		y[x > nn[-2]] = np.nan
		line_gap, spacing = .1, .1
		
		off = y * 0.
		for j in np.arange(len(bnry)):
			off[(nn[j] <= x) & (x < nn[j + 1])] = int(bnry[j])
		y1 = np.copy(y)
		y1[off == 0] = np.nan
		minoff = [min(last - np.roll(y, i)) for i in np.arange(len(y))]
		offset = max(minoff) - spacing
		iroll = np.where(minoff == max(minoff))[0][0]
		y, y1 = np.roll(y, iroll), np.roll(y1, iroll)
		
		yplot, y1plot = y + offset, y1 + offset - line_gap
		plt.plot(x, yplot, '#6b8e23')
		plt.plot(x, y1plot, '#6b8e23')
		plt.plot([x[iroll], (xx[-1] + x[iroll]) % 1], [alt_norm[0] + offset, alt_norm[-1] + offset], 'o', c='#6b8e23',
		         ms=3)
		
		last = yplot - line_gap
	plt.axvline(x=0, linestyle='--', color='k', alpha=0.5)
	plt.axvline(x=1, linestyle='--', color='k', alpha=0.5)


if __name__ == '__main__':
	# original()
	minimize_offset()
	plt.show()
