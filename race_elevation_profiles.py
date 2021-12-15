import gpxpy
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

dir = 'C:/Users/Owner/PycharmProjects/Sandbox/data/'
k50 = dir + 'superior_spring_50k.gpx'
m50 = dir + 'stone_mill_50M.gpx'

fig = plt.figure(figsize=[14.5, 2])
plt.axis('off')
plt.tight_layout()
for i, (lbl, file) in enumerate([('superior50k2018', k50), ('stonemill50M2020', m50)]):
    f = open(file, 'r')
    gpx = gpxpy.parse(f)
    pts = gpx.tracks[0].segments[0].points
    alt = [pt.elevation for pt in pts]
    alt_norm = (alt - np.min(alt)) / np.max(alt - np.min(alt))
    alt_norm = [a - alt[0] for a in alt]
    xx = np.linspace(0, 1, num=len(alt_norm))
    x = np.linspace(0, 1, num=250)
    y = np.interp(x, xx, alt_norm)

    # bnry = bin(int.from_bytes(lbl.encode(), 'big'))[2:]  # makes no sense, uninterpretable
    o = [ord(l) - 97 if ord(l) >= 97 else int(l) for l in
         lbl.lower()]  # make lowercase then make a=0,b=1,... mapping leaving numbers as numbers
    bnry = ''.join([bin(l)[2:].zfill(5) for l in o])  # give each char 5 digits and convert to binary
    print(lbl + ': ' + bnry)
    # original
    # plt.plot(x, y + i * .85, '#6b8e23', label=lbl, alpha=0.75)

    cross_height = 10
    offset = [0, -50]
    shadow = 1
    linestyle = 0

    if shadow:  # linethick
        nn = np.linspace(0, 1, num=len(bnry) + 1)
        off = y * 0.
        for j in np.arange(len(bnry)):
            off[(nn[j] <= x) & (x <= nn[j + 1])] = int(bnry[j])
        y1 = np.copy(y)
        y1[off == 0] = np.nan
        # y[x <= nn[1]], y1[x <= nn[1]] = np.nan, np.nan
        plt.plot(x, y + offset[i], '#6b8e23')
        plt.plot(x, y1 + offset[i], '#6b8e23', path_effects=[pe.SimpleLineShadow(offset=(0, -2)), pe.Normal()])
        plt.plot([nn[1], nn[1]], [np.interp(nn[1], x, y) + offset[i] - cross_height,
                                  np.interp(nn[1], x, y) + offset[i] + cross_height], '#6b8e23')

    if linestyle:
        nn = np.linspace(0, 1, num=len(bnry) + 1)
        off = y * 0.
        for j in np.arange(len(bnry)):
            off[(nn[j] <= x) & (x <= nn[j + 1])] = int(bnry[j])
        y1 = np.copy(y)
        y1[off == 0] = np.nan
        plt.plot(x, y + offset[i], '#6b8e23', linestyle=':')
        plt.plot(x, y1 + offset[i], '#6b8e23')
        plt.plot([nn[1], nn[1]], [np.interp(nn[1], x, y) + offset[i] - cross_height,
                                  np.interp(nn[1], x, y) + offset[i] + cross_height], '#6b8e23')

    # small offset
    # nn = np.linspace(0, 1, num=len(bnry) + 1)
    # off = y * 0.
    # for j in np.arange(len(bnry)):
    #     off[(nn[j] <= x) & (x <= nn[j + 1])] = int(bnry[j])
    # y0, y1 = np.copy(y), np.copy(y)+.1
    # y0[off == 1], y1[off == 0] = np.nan, np.nan
    # plt.plot(x, y0 + i * .85, '#6b8e23', label=lbl, alpha=0.75)
    # plt.plot(x, y1 + i * .85, '#6b8e23', label=lbl, alpha=0.75)
    # plt.plot(nn[1], np.interp(nn[1], x, y) + int(bnry[0])*.1, '+')

    # markers
    # nn = np.linspace(0, 1, num=len(bnry) + 2)
    # x1 = [nn[i] for i in np.arange(len(bnry)) if int(bnry[i]) == 1]
    # x0 = [nn[i] for i in np.arange(len(bnry)) if int(bnry[i]) == 0]
    # plt.plot(x1, np.interp(x1, x, y)+ i * .85, '+')
    # plt.plot(x0, np.interp(x0, x, y)+ i * .85, 'o')
# plt.legend()
plt.show()
