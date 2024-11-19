import matplotlib.pyplot as plt
import numpy as np
import gpxpy
import geopy.distance as dist

clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']
m_per_mi = 1609.34
direc = 'C:/Users/wcapecch/Dropbox/running_stuff/Zion_2023/'


def write_gpx(lat, lon, outfn):
	outgpx = gpxpy.gpx.GPX()
	gpxtrack = gpxpy.gpx.GPXTrack()
	outgpx.tracks.append(gpxtrack)
	gpxseg = gpxpy.gpx.GPXTrackSegment()
	gpxtrack.segments.append(gpxseg)
	assert len(lat) == len(lon)
	for i in np.arange(len(lat)):
		gpxseg.points.append(gpxpy.gpx.GPXTrackPoint(lat[i], lon[i]))  # (lat, lon, elev)  - no elev data for this file
	print(f'creating gpx: {outfn}.gpx')
	with open(f'{outfn}.gpx', 'w') as f:
		f.write(outgpx.to_xml())


def breakup_route():
	gpxfn = f'{direc}Zion_100mi.gpx'
	f = open(gpxfn, 'r')
	gpx = gpxpy.parse(f)
	pts = gpx.tracks[0].segments[0].points
	'''compute distance (input is [lat, long])'''
	latlon = np.array([[pt.latitude for pt in pts], [pt.longitude for pt in pts]])
	# remove (lots of) duplicate points
	ii = [i + 1 for i in np.arange(len(latlon[0, :]) - 1) if all(latlon[:, i] != latlon[:, i + 1])]
	ii.insert(0, 0)  # put in first point
	latlon = latlon[:, ii]
	dis = np.array([dist.distance(latlon[:, i], latlon[:, i + 1]).m for i in np.arange(len(latlon[0]) - 1)])  # m
	cumdist_mile = np.append(0, np.cumsum(dis / m_per_mi))
	
	# do all single passthroughs first
	indexcheck = np.arange(len(latlon[0, :]))
	desert_latlon = [37.178535, -113.238808]
	dis = np.array([dist.distance(latlon[:, i], desert_latlon).m for i in indexcheck])
	idesert = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
	print(f'desert at mile {cumdist_mile[idesert]:.2f}')
	
	dam_latlon = [37.196379, -113.235089]
	dis = np.array([dist.distance(latlon[:, i], dam_latlon).m for i in indexcheck])
	idam = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
	print(f'dam at mile {cumdist_mile[idam]:.2f}')
	
	smith_latlon = [37.241714, -113.203272]
	dis = np.array([dist.distance(latlon[:, i], smith_latlon).m for i in indexcheck])
	ismith = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
	print(f'smith at mile {cumdist_mile[ismith]:.2f}')
	
	# go through multi-pass AS
	strt_latlon = [37.115755, -113.109512]
	istrt, indexcheck = [], np.arange(len(latlon[0, :]))
	for i in np.arange(3):  # 3 passes through start
		dis = np.array([dist.distance(latlon[:, i], strt_latlon).m for i in indexcheck])
		igb = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
		istrt.append(igb)
		print(f'start at mile {cumdist_mile[igb]:.2f}')
		indexcheck = indexcheck[np.where(abs(cumdist_mile[indexcheck] - cumdist_mile[igb]) > 5)]
	istrt.sort()  # order by distance
	
	goosebump_latlon = [37.156888, -113.166757]
	igoosebump, indexcheck = [], np.arange(len(latlon[0, :]))
	for i in np.arange(3):  # 3 passes through goosebump
		dis = np.array([dist.distance(latlon[:, i], goosebump_latlon).m for i in indexcheck])
		igb = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
		igoosebump.append(igb)
		print(f'goosebump at mile {cumdist_mile[igb]:.2f}')
		indexcheck = indexcheck[np.where(abs(cumdist_mile[indexcheck] - cumdist_mile[igb]) > 5)]
	igoosebump.sort()  # order by distance
	
	bmx_latlon = [37.213051, -113.176625]
	ibmx, indexcheck = [], np.arange(len(latlon[0, :]))
	for i in np.arange(2):  # 2 passes through bmx
		dis = np.array([dist.distance(latlon[:, i], bmx_latlon).m for i in indexcheck])
		igb = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
		ibmx.append(igb)
		print(f'bmx at mile {cumdist_mile[igb]:.2f}')
		indexcheck = indexcheck[np.where(abs(cumdist_mile[indexcheck] - cumdist_mile[igb]) > 5)]
	ibmx.sort()  # order by distance
	
	guac_latlon = [37.226234, -113.114620]
	iguac, indexcheck = [], np.arange(len(latlon[0, :]))
	for i in np.arange(2):  # 2 passes through guac
		dis = np.array([dist.distance(latlon[:, i], guac_latlon).m for i in indexcheck])
		igb = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
		iguac.append(igb)
		print(f'guac at mile {cumdist_mile[igb]:.2f}')
		indexcheck = indexcheck[np.where(abs(cumdist_mile[indexcheck] - cumdist_mile[igb]) > 5)]
	iguac.sort()  # order by distance
	
	grafton_latlon = [37.130926, -113.098023]
	igrafton, indexcheck = [], np.arange(len(latlon[0, :]))
	for i in np.arange(3):  # 3 passes through grafton
		dis = np.array([dist.distance(latlon[:, i], grafton_latlon).m for i in indexcheck])
		igb = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
		igrafton.append(igb)
		print(f'grafton at mile {cumdist_mile[igb]:.2f}')
		indexcheck = indexcheck[np.where(abs(cumdist_mile[indexcheck] - cumdist_mile[igb]) > 5)]
	igrafton.sort()  # order by distance
	
	wire_latlon = [37.132878, -113.071139]
	iwire, indexcheck = [], np.arange(len(latlon[0, :]))
	for i in np.arange(2):  # 2 passes through wire
		dis = np.array([dist.distance(latlon[:, i], wire_latlon).m for i in indexcheck])
		igb = indexcheck[np.where(dis == np.nanmin(dis))[0][0]]  # index of close approach
		iwire.append(igb)
		print(f'wire at mile {cumdist_mile[igb]:.2f}')
		indexcheck = indexcheck[np.where(abs(cumdist_mile[indexcheck] - cumdist_mile[igb]) > 5)]
	iwire.sort()  # order by distance
	
	a = 1
	# start to virgin desert
	i1, i2, ofn = istrt[0], idesert + 1, f'{direc}z1_strt_vdes'
	write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)

	# virgin desert to virgin BMX 1
	i1, i2, ofn = idesert, ibmx[0] + 1, f'{direc}z2_vdes_vbmx1'
	write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)

	# virgin BMX 1-2
	i1, i2, ofn = ibmx[0], ibmx[1] + 1, f'{direc}z3_vbmx1_vbmx2'
	write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)

	# virgin BMX 2-crew
	i1, i2, ofn = ibmx[1], istrt[1] + 1, f'{direc}z4_vbmx2_crew'
	write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)

	# crew-finish
	i1, i2, ofn = istrt[1], istrt[2] + 1, f'{direc}z5_crew_fin'
	write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	
	# # start 1 to goosebump 1
	# i1, i2, ofn = istrt[0], igoosebump[0] + 1, f'{direc}s01_strt_goose1'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # goosebump 1 to goosebump 2
	# i1, i2, ofn = igoosebump[0], igoosebump[1] + 1, f'{direc}s02_goose1_goose2'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # goosebump 2 to virgin desert
	# i1, i2, ofn = igoosebump[1], idesert + 1, f'{direc}s03_goose2_desert'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # virgin desert to virgin dam
	# i1, i2, ofn = idesert, idam + 1, f'{direc}s04_desert_dam'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # virgin dam to smith mesa
	# i1, i2, ofn = idam, ismith + 1, f'{direc}s05_dam_smith'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # smith mesa to virgin bmx1
	# i1, i2, ofn = ismith, ibmx[0] + 1, f'{direc}s06_smith_bmx1'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # virgin bmx 1 to guacamole 1
	# i1, i2, ofn = ibmx[0], iguac[0] + 1, f'{direc}s07_bmx1_guac1'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # guacamole 1 to guacamole 2
	# i1, i2, ofn = iguac[0], iguac[1] + 1, f'{direc}s08_guac1_guac2'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # guacamole 2 to bmx 2
	# i1, i2, ofn = iguac[1], ibmx[1] + 1, f'{direc}s09_guac2_bmx2'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # bmx 2 to goosebump 3
	# i1, i2, ofn = ibmx[1], igoosebump[2] + 1, f'{direc}s10_bmx2_goose3'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # goosebump 3 to start 2
	# i1, i2, ofn = igoosebump[2], istrt[1] + 1, f'{direc}s11_goose3_strt'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # start 2 to grafton 1
	# i1, i2, ofn = istrt[1], igrafton[0] + 1, f'{direc}s12_strt_grafton1'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # grafton 1 to wire 1
	# i1, i2, ofn = igrafton[0], iwire[0] + 1, f'{direc}s13_grafton1_wire1'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # wire 1 to wire 2
	# i1, i2, ofn = iwire[0], iwire[1] + 1, f'{direc}s14_wire1_wire2'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # wire 2 to grafton 2
	# i1, i2, ofn = iwire[1], igrafton[1] + 1, f'{direc}s15_wire2_grafton2'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # grafton 2 to grafton 3
	# i1, i2, ofn = igrafton[1], igrafton[2] + 1, f'{direc}s16_grafton2_grafton3'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # grafton 3 to finish
	# i1, i2, ofn = igrafton[2], istrt[2] + 1, f'{direc}s17_grafton3_finish'
	# write_gpx(latlon[0, i1:i2], latlon[1, i1:i2], ofn)
	# # full route
	# write_gpx(latlon[0, :], latlon[1, :], f'{direc}zion_full')


if __name__ == '__main__':
	breakup_route()
