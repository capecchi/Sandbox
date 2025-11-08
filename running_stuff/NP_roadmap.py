import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import requests
import polyline
import folium

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

home = [44.9, -93.18]  # latlon
m_per_mile = 1609.34
direc = f'C:/Users/willi/PycharmProjects/Sandbox/running_stuff/data/'
mapbox_token = 'pk.eyJ1IjoiY2FwZWNjaGkiLCJhIjoiY2owNzV0YzdzMHFiYzJxbHNnbTJuZ2h3diJ9.ArYGu-QKz3D8D0oZLyvgSA'
params = {
    "access_token": mapbox_token,
    "overview": "full",
    "geometries": "polyline",
    "alternatives": "false",
}


def get_route(pickup_latlon, dropoff_latlon):
    (pickup_lat, pickup_lon), (dropoff_lat, dropoff_lon) = pickup_latlon, dropoff_latlon
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{loc}"
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return {'ok': False}
    res = r.json()
    if res['code'] != 'Ok':
        return {'ok': False}
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    dist, dur = res['routes'][0]['distance'] / m_per_mile, res['routes'][0]['duration'] / 3600.  # [hr]
    out = {'route': routes, 'start_point': start_point, 'end_point': end_point, 'distance': dist, 'duration': dur,
           'ok': True}
    return out


class NP:
    def __init__(self, latlons):
        self.coords = latlons[:2]
        self.visitor_center = latlons[2:]


def np_info():
    #  [park_lat, park_lon, visitor center lat, visitor center lon]
    natl_parks = {
        'Acadia': NP([44.35, -68.21, 44.409481, -68.248107]),
        'American Samoa': NP([-14.25, -170.68, -14.274221, -170.696928]),
        'Arches': NP([38.68, -109.57, 38.616145, -109.620168]),
        'Badlands': NP([43.75, -102.5, 43.748389, -101.941516]),
        'Big Bend': NP([29.25, -103.25, 29.328206, -103.206099]),
        'Biscayne': NP([25.65, -80.08, 25.464200, -80.335065]),
        'Black Canyon\nof the Gunnison': NP([38.57, -107.72, 38.554824, -107.686392]),
        'Bryce Canyon': NP([37.57, -112.18, 37.640370, -112.169072]),
        'Canyonlands': NP([38.2, -109.93, 38.460497, -109.820945]),
        'Capitol Reef': NP([38.2, -111.17, 38.290981, -111.261704]),
        'Carlsbad Caverns': NP([32.17, -104.44, 32.174746, -104.443696]),
        'Channel Islands': NP([34.01, -119.42, 34.246818, -119.267030]),
        'Congaree': NP([33.78, -80.78, 33.830187, -80.823199]),
        'Crater Lake': NP([42.94, -122.1, 42.896730, -122.134045]),
        'Cuyahoga Valley': NP([41.24, -81.55, 41.261805, -81.560210]),
        'Death Valley': NP([36.24, -116.82, 36.461394, -116.866814]),
        'Denali': NP([63.33, -150.5, 63.730850, -148.918521]),
        'Dry Tortugas': NP([24.63, -82.87, 24.562699, -81.799028]),
        'Everglades': NP([25.32, -80.93, 25.395107, -80.583735]),
        'Gates of the Arctic': NP([67.78, -153.3, 67.252595, -150.185783]),
        'Gateway Arch': NP([38.63, -90.19, 38.625314, -90.187113]),
        'Glacier': NP([48.8, -114., 48.748201, -113.439320]),
        'Glacier Bay': NP([58.5, -137., 58.454411, -135.882385]),
        'Grand Canyon': NP([36.06, -112.14, 36.056966, -112.109236]),
        'Grand Teton': NP([43.73, -110.8, 43.654706, -110.716672]),
        'Great Basin': NP([38.98, -114.3, 39.014310, -114.126556]),
        'Great Sand Dunes': NP([37.73, -105.51, 37.732271, -105.511617]),
        'Great Smoky\nMountains': NP([35.68, -85.53, 35.685175, -83.536687]),
        'Guadalupe\nMountains': NP([31.92, -104.87, 31.893617, -104.822087]),
        'Haleakala': NP([20.72, -156.17, 20.759647, -156.246282]),
        'Hawaii Volcanoes': NP([19.38, -155.2, 19.429457, -155.257503]),
        'Hot Springs': NP([34.51, -93.05, 34.513752, -93.053884]),
        'Indiana  Dunes': NP([41.6533, -87.0524, 41.632872, -87.054193]),
        'Isle Royale': NP([48.1, -88.55, 47.960499, -89.686198]),
        'Joshua Tree': NP([33.79, -115.9, 34.134113, -116.315226]),
        'Katmai': NP([58.5, -155., 58.553716, -155.778530]),
        'Kenai Fjords': NP([59.92, -149.65, 60.116299, -149.440367]),
        'Kings Canyon': NP([36.8, -118.55, 36.740150, -118.963706]),
        'Kobuk Valley': NP([67.55, -159.28, 66.892366, -162.604637]),
        'Lake Clark': NP([60.97, -153.42, 60.197234, -154.322996]),
        'Lassen Volcanic': NP([40.49, -121.51, 40.437468, -121.534156]),
        'Mammoth Cave': NP([37.18, -86.1, 37.187244, -86.099541]),
        'Mesa Verde': NP([37.18, -108.49, 37.339143, -108.411888]),
        'Mount Rainier': NP([46.85, -121.75, 46.785561, -121.736662]),
        'New River Gorge': NP([38.07, -81.08, 38.071925, -81.074844]),
        'North Cascades': NP([48.7, -121.2, 48.666123, -121.264865]),
        'Olympic': NP([47.97, -123.5, 48.099567, -123.425712]),
        'Petrified Forest': NP([35.07, -109.78, 35.066008, -109.782933]),
        'Pinnacles': NP([36.48, -121.16, 36.493607, -121.146832]),
        'Redwood': NP([41.3, -124.0, 41.283661, -124.091086]),
        'Rocky Mountain': NP([40.4, -105.58, 40.367472, -105.562753]),
        'Saguaro': NP([32.25, -110.5, 32.179930, -110.736338]),
        'Sequoia': NP([36.43, -118.68, 36.603830, -118.734470]),
        'Shenandoah': NP([38.53, -78.35, 38.517259, -78.436601]),
        'Theodore\nRoosevelt': NP([46.97, -103.45, 46.893808, -103.382943]),
        'Virgin Islands': NP([18.33, -64.73, 18.332937, -64.793764]),
        'Voyageurs': NP([48.444261, -93.030371, 48.434504, -92.849040]),
        'White Sands': NP([32.78, -106.17, 32.778846, -106.172155]),
        'Wind Cave': NP([43.57, -103.48, 43.554273, -103.477615]),
        'Wrangell-\nSt. Elias': NP([61.0, -142.0, 62.020553, -145.364016]),
        'Yellowstone': NP([44.6, -110.5, 44.460916, -110.844029]),
        'Yosemite': NP([37.83, -119.5, 37.745122, -119.583220]),
        'Zion': NP([37.3, -113.05, 37.200667, -112.986118])
    }
    # natl_parks = {
    #     'Acadia': [44.409481, -68.248107],
    #     'Arches': [38.616145, -109.620168],
    #     'Badlands': [43.748389, -101.941516],
    #     'Big Bend': [29.328206, -103.206099],
    #     'Biscayne': [25.464200, -80.335065],
    #     'Black Canyon\nof the Gunnison': [38.554824, -107.686392],
    #     'Bryce Canyon': [37.640370, -112.169072],
    #     'Canyonlands': [38.460497, -109.820945]
    # }

    return natl_parks


def generate_routes(maponly=False):
    npmap = folium.Map(location=home, zoom_start=5, tiles='OpenStreetMap')  # 'CartoDB positron'
    locs = np_info()
    loc_names = [k for k in locs.keys()]
    loc_names.insert(0, 'HOME')  # put home first
    locs['HOME'] = NP([np.nan, np.nan, home[0], home[1]])
    nn = len(loc_names)
    dat = np.zeros((nn, nn))
    for i, k1 in enumerate(loc_names):
        v1 = locs[k1].visitor_center  # latlon of visitor center at location 1
        if maponly and i > 0:
            break
        for j, k2 in enumerate(loc_names):
            print(f'{i},{j} :: {nn}')
            if j <= i:
                dat[j, i] = np.nan
            else:
                v2 = locs[k2].visitor_center  # latlon of visitor center at location 2
                o = get_route(v1, v2)
                if o['ok']:
                    dat[j, i] = o['duration']  # o['distance']]
                else:
                    dat[j, i] = np.nan
                if k1 == 'HOME':  # only map stuff from home
                    if o['ok']:
                        pop = f'{k2}\n{o["distance"]:.0f}_mi\n{o["duration"]:.1f} hrs'
                        folium.PolyLine(o['route']).add_to(npmap)
                    else:
                        pop = f'{k2}'
                        print(f'issue computing route for {k2}')
                    folium.Marker(location=locs[k2].coords, popup=pop,
                                  icon=folium.Icon(icon='tree-conifer', color='lightgray')).add_to(npmap)
    folium.Marker(location=home, popup='Home', icon=folium.Icon(color='green', icon='home')).add_to(npmap)
    if not maponly:
        df = pd.DataFrame(dat, columns=loc_names)
        df.to_csv(f'{direc}npdata.csv', index=False)
        print('data saved')
    npmap.save(f'{direc}npmap.html')
    print('map saved')


def plot_table():
    dat = pd.read_csv(f'{direc}npdata.csv')
    cols = dat.columns
    vals = dat.values

    igoodcols = []
    for i in np.arange(len(vals)):
        if not all([np.isnan(v) for v in np.append(vals[i, :], vals[:, i])]):  # look for rows+columns with all nans
            igoodcols.append(i)

    vals = dat[cols[igoodcols]].values[igoodcols, :]  # get rid of rows/columns with only nans
    goodcols = cols[igoodcols]

    cell_text = np.array(
        [[f'{round(item)}' if not np.isnan(item) else '' for item in row] if isinstance(row, list) else [
            f'{round(item)}' if not np.isnan(item) else '' for item in row] for row in vals])

    norm = plt.Normalize(np.nanmin(vals) - 1, np.nanmax(vals) + 1)
    colours = plt.cm.RdYlGn_r(norm(vals))

    fig, ax = plt.subplots(figsize=(15, 15))

    # figure out correct fontsize
    t = ax.text(0, 0.5, '1.0', fontsize=10, va='center')
    fig.canvas.draw()  # Needed to compute text bounding box
    bbox = t.get_window_extent(renderer=fig.canvas.get_renderer())
    data_height = ax.transData.inverted().transform([(0, bbox.y1), (0, bbox.y0)])
    text_data_height = abs(data_height[0][1] - data_height[0][0])
    scale = 1. / text_data_height
    fs = .8 * (10 * scale)
    t.set_visible(False)

    for i, row in enumerate(vals):
        for j in np.arange(len(goodcols)):
            if cell_text[i, j] != '':
                ax.fill_between([j, j + 1], -i, -i - 1, color=colours[i, j, :])
                ax.text(j + .5, -i - .5, cell_text[i, j], fontsize=fs, va='center', ha='center')

    ax.set_xlim((0, len(goodcols) - 1))  # have to set x/y limits here after figuring out fontsize
    ax.set_ylim((-len(goodcols), -1))
    ax.set_yticks(-np.arange(len(goodcols) - 1) - 1.5, labels=goodcols[1:])
    ax.set_xticks(np.arange(len(goodcols) - 1) + .5, labels=goodcols[:-1], rotation=90)
    ax.spines[['right', 'top']].set_visible(False)
    plt.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(25, 6))
    hvals = vals[1:, 0]  # home values
    hcols = goodcols[1:]
    sp = sorted(zip(hvals, hcols))
    hvals_sorted = [v for v, k in sp]
    hcols_sorted = [k for v, k in sp]
    ax2.plot(np.arange(len(hvals)), hvals_sorted, 'o-')
    ax2.set_xticks(np.arange(len(hcols)), labels=hcols_sorted, rotation=90)
    ax2.vlines(np.arange(len(hcols)), np.zeros_like(hcols), hvals_sorted, colors='k', linestyles='--', alpha=0.5)
    ax2.set_ylabel('travel time (hrs)')
    ax2.set_ylim(bottom=0)
    ax2.set_xlim((-.5, len(hcols) - .5))
    ax2.hlines([10, 20, 30, 40, 50, 60], np.zeros(6) - .5, np.ones(6) * len(hcols), colors='k', alpha=.2)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # generate_routes(maponly=True)
    plot_table()
