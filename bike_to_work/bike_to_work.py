import re
import os
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import folium
import polyline
from scipy.interpolate import griddata
import geojsoncontour
from folium.features import DivIcon
import scipy.ndimage as ndi


def its_a_square():
	# if looking for, say, 10 mile bike to work
	# can't bike straight there, have to follow roads
	# make assumption most roads are on a grid
	
	theta = np.linspace(0, 2 * np.pi, num=1000, endpoint=True)
	bike_max = 1.  #
	r = bike_max / (abs(np.cos(theta)) + abs(np.sin(theta)))
	# plt.plot(theta,np.cos(theta))
	# plt.plot(theta,np.sin(theta))
	
	plt.plot(bike_max * np.cos(theta), bike_max * np.sin(theta), label='circle')
	plt.plot(r * np.cos(theta), r * np.sin(theta), label='bike-limit')
	plt.legend()
	plt.tight_layout()
	plt.show()


def madison_crowflies_map():
	direc = 'C:/Users/wcapecch/PycharmProjects/Sandbox/'
	psl = (42.96038948982479, -89.28999921687905)
	chambo = (43.074080288441515, -89.40598185117018)
	madmap = folium.Map(location=[np.mean([psl[0], chambo[0]]), np.mean([psl[1], chambo[1]])],
	                    zoom_start=12, tiles='CartoDB positron')
	rad_miles = [2, 4, 6, 8, 10, 12, 14]
	mile_2_meters = 1609.34  # m per mile
	rad_meters = [rm * mile_2_meters for rm in rad_miles]
	folium.Marker(location=psl, tooltip='PSL').add_to(madmap)
	folium.Marker(location=chambo, tooltip='Chamberlin').add_to(madmap)
	for (rmet, rmil) in zip(rad_meters, rad_miles):
		folium.Circle(location=psl, radius=rmet, color='red', opacity=.5, tooltip=f'{rmil} Miles from PSL').add_to(
			madmap)
		folium.Circle(location=chambo, radius=rmet, color='blue', opacity=.5,
		              tooltip=f'{rmil} Miles from Chamberlin').add_to(
			madmap)
	madmap.save(f'{direc}madmap.html')


def madison_map(redo=False):
	direc = 'C:/Users/wcapecch/PycharmProjects/Sandbox/bike_to_work/'
	num = 50
	psl = (42.96038948982479, -89.28999921687905)
	chambo = (43.074080288441515, -89.40598185117018)
	dlat = .3
	dlon = .3
	meters_per_mile = 1609.34  # m per mile
	lat = np.linspace(min([psl[0], chambo[0]]) - dlat, max([psl[0], chambo[0]]) + dlat, endpoint=True, num=num)
	lon = np.linspace(min([psl[1], chambo[1]]) - dlon, max([psl[1], chambo[1]]) + dlon, endpoint=True, num=num)
	# lon = np.linspace(min([psl[1], chambo[1]]) - dlon, min([psl[1], chambo[1]]), endpoint=True, num=5)
	latt, longg = np.meshgrid(lat, lon)
	
	def get_route(pickup_latlon, dropoff_latlon):
		(pickup_lat, pickup_lon), (dropoff_lat, dropoff_lon) = pickup_latlon, dropoff_latlon
		loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
		url = "http://router.project-osrm.org/route/v1/driving/"
		r = requests.get(url + loc)
		if r.status_code != 200:
			return {}
		res = r.json()
		routes = polyline.decode(res['routes'][0]['geometry'])
		start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
		end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
		distance = res['routes'][0]['distance']
		out = {'route': routes, 'start_point': start_point, 'end_point': end_point, 'distance': distance}
		return out
	
	# if don't exist, create file
	if redo or not os.path.isfile(f'{direc}mapdata.json'):
		inlat, inlon = [], []
		psl_outlat, psl_outlon, psl_dist = [], [], []
		chambo_outlat, chambo_outlon, chambo_dist = [], [], []
		tempdict = {'inlat': inlat, 'inlon': inlon, 'psl_outlat': psl_outlat, 'psl_outlon': psl_outlon,
		            'psl_dist': psl_dist, 'chambo_outlat': chambo_outlat, 'chambo_outlon': chambo_outlon,
		            'chambo_dist': chambo_dist}
		with open(f'{direc}mapdata.json', 'w') as wf:
			json.dump(tempdict, wf)
	
	with open(f'{direc}mapdata.json') as jfile:
		dat = json.load(jfile)
	inlat, inlon = dat['inlat'], dat['inlon']
	psl_outlat, psl_outlon, psl_dist = dat['psl_outlat'], dat['psl_outlon'], dat['psl_dist']
	chambo_outlat, chambo_outlon, chambo_dist = dat['chambo_outlat'], dat['chambo_outlon'], dat['chambo_dist']
	
	lat2do, lon2do = [], []
	for i in range(len(lat)):
		for j in range(len(lon)):
			if len(np.where((np.array(inlat) == lat[i]) & (np.array(inlon) == lon[j]))[0]) < 1:
				lat2do.append(lat[i])
				lon2do.append(lon[j])
	saveticker = 0
	for icoord in range(len(lat2do)):
		print(f'{(icoord + 1)}/{len(lat2do)}')
		p = get_route(psl, (lat2do[icoord], lon2do[icoord]))
		c = get_route(chambo, (lat2do[icoord], lon2do[icoord]))
		inlat.append(lat2do[icoord])
		inlon.append(lon2do[icoord])
		psl_outlat.append(p['end_point'][0])
		psl_outlon.append(p['end_point'][1])
		psl_dist.append(p['distance'])
		chambo_outlat.append(c['end_point'][0])
		chambo_outlon.append(c['end_point'][1])
		chambo_dist.append(c['distance'])
		saveticker += 1
		if saveticker >= 50 or icoord == len(lat2do) - 1:
			saveticker = 0
			savedict = {'inlat': inlat, 'inlon': inlon, 'psl_outlat': psl_outlat, 'psl_outlon': psl_outlon,
			            'psl_dist': psl_dist, 'chambo_outlat': chambo_outlat, 'chambo_outlon': chambo_outlon,
			            'chambo_dist': chambo_dist}
			with open(f'{direc}mapdata.json', 'w') as wf:
				json.dump(savedict, wf)
			print('--updated file--')
	
	psl_mesh = griddata((psl_outlat, psl_outlon), psl_dist, (latt, longg), method='cubic')
	chambo_mesh = griddata((chambo_outlat, chambo_outlon), chambo_dist, (latt, longg), method='cubic')
	psl_mesh2 = ndi.gaussian_filter(psl_mesh, sigma=1.0, order=0)
	chambo_mesh2 = ndi.gaussian_filter(chambo_mesh, sigma=1.0, order=0)
	
	fig, ax = plt.subplots()
	levs = [2, 4, 6, 8, 10, 12, 14]
	psl_cont = ax.contour(longg, latt, psl_mesh2 / meters_per_mile, levels=levs)
	chambo_cont = ax.contour(longg, latt, chambo_mesh2 / meters_per_mile, levels=levs)
	# plt.show()
	# fig2, ax2 = plt.subplots()
	# ax2.plot(psl_outlon, psl_outlat, 'o')
	# dolabels = [ax2.annotate(f'{psl_dist[i]}',(psl_outlon[i],psl_outlat[i])) for i in range(len(psl_outlon))]
	# plt.show()
	
	psl_geo = geojsoncontour.contour_to_geojson(contour=psl_cont, ndigits=5)  # , unit='m')
	chambo_geo = geojsoncontour.contour_to_geojson(contour=chambo_cont, ndigits=5)  # , unit='m')
	with open(f'psl_geo.json', 'w') as out:
		json.dump(psl_geo, out)
	with open(f'chambo_geo.json', 'w') as out:
		json.dump(chambo_geo, out)
	print(f'saved new maps')
	madmap = folium.Map(location=[np.mean([psl[0], chambo[0]]), np.mean([psl[1], chambo[1]])],
	                    zoom_start=11, tiles='OpenStreetMap')  # 'CartoDB positron'
	folium.GeoJson(psl_geo).add_to(
		madmap)  # , style_function=lambda x: {'color': 'green', 'opacity': .5}).add_to(madmap)
	folium.GeoJson(chambo_geo).add_to(
		madmap)  # , style_function=lambda x: {'color': 'blue', 'opacity': .5}).add_to(madmap)
	
	for (lbl, geo) in zip(['p', 'c'], [psl_geo, chambo_geo]):
		geodict = json.loads(geo)
		for feat in geodict['features']:
			lev = feat['properties']['level-value']
			lonlat = feat['geometry']['coordinates'][0]
			folium.map.Marker([lonlat[1], lonlat[0]], icon=DivIcon(icon_size=(150, 36), icon_anchor=(0, 0),
			                                                       html=f'<div style="font-size: 12pt">{lev}{lbl}</div>', )).add_to(
				madmap)
	folium.Marker(location=psl, icon=folium.Icon(color='green')).add_to(madmap)
	folium.Marker(location=chambo, icon=folium.Icon(icon='play', color='blue')).add_to(madmap)
	madmap.save(f'{direc}madmap.html')
	print(f'...done mapping stuff')


# plt.show()


def test_map():
	psl = (42.96038948982479, -89.28999921687905)
	chambo = (43.074080288441515, -89.40598185117018)
	m = folium.Map(location=chambo, zoom_start=9)
	num = 100
	psl = (42.96038948982479, -89.28999921687905)
	chambo = (43.074080288441515, -89.40598185117018)
	dlat = .3
	dlon = .2
	meters_per_mile = 1609.34  # m per mile
	lat = np.linspace(min([psl[0], chambo[0]]) - dlat, max([psl[0], chambo[0]]) + dlat, endpoint=True, num=num)
	lon = np.linspace(min([psl[1], chambo[1]]) - dlon, max([psl[1], chambo[1]]) + dlon, endpoint=True, num=num)
	latt, longg = np.meshgrid(lat, lon)
	z = np.zeros_like(latt)
	for i in range(len(lat)):
		for j in range(len(lon)):
			z[j, i] = np.sqrt((lat[i] - psl[0]) ** 2 + (lon[j] - psl[1]) ** 2)
	
	fig, ax = plt.subplots()
	cont = ax.contour(longg, latt, z, levels=np.linspace(0, .6, num=25))
	psl_geo = geojsoncontour.contour_to_geojson(contour=cont, ndigits=5)  # , unit='m')
	folium.GeoJson(psl_geo, style_function=lambda x: {'color': 'green', 'opacity': .5}).add_to(m)
	# ax.plot(psl[1], psl[0], 'o')
	# plt.show()
	folium.Marker(location=psl).add_to(m)
	folium.Marker(location=chambo).add_to(m)
	direc = 'C:/Users/wcapecch/PycharmProjects/Sandbox/bike_to_work/'
	m.save(f'{direc}madmap2.html')


if __name__ == '__main__':
	# its_a_square()
	# madison_crowflies_map()
	madison_map(redo=False)
	# test_map()
	pass
