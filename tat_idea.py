import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Rectangle

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

mtn = []  # array of pts to simulate mtn
MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}


def horizontal(word):
    pct = 1 / 3.  # fraction a dot occupies
    dashlength = 1
    linespacing = 1
    linewidth = .2 * linespacing

    endpts = []
    for ilett, letter in enumerate(word):
        xlett = 0
        ylett = -ilett * linespacing
        mrs = MORSE_CODE_DICT[letter]
        for idit, ditdash in enumerate(mrs):
            if ditdash == '.':
                xlett1, xwid = idit * dashlength + dashlength * pct, dashlength * pct
            else:
                xlett1, xwid = idit * dashlength, dashlength
            endpts.append([xlett1 - len(mrs), ylett, xwid])
    endpts = np.array(endpts)

    fig, ax = plt.subplots()
    for segs in endpts:
        ax.add_patch(Rectangle((segs[0], segs[1]), segs[2], linewidth, color='k', alpha=.5, edgecolor=None))

    plt.xlim((-4, 0))
    plt.ylim(((-4.5, .5)))
    plt.show()


def vertical(word):
    fig, ax = plt.subplots()
    pct = 1 / 3.  # fraction a dot occupies
    dashlength = 1
    yspacing = .4 * dashlength
    xspacing = np.cumsum(np.array([0., .6, .8, .3, .7]) * dashlength)
    linewidth = .2 * yspacing
    yoff = np.array([0, 2, 1, -1.7, -.2]) * yspacing
    trunks = np.array([5.5, 6, 6, 3, 5]) * yspacing

    c_arr, endpts = [], []
    for ilett, letter in enumerate(word):
        xlett = xspacing[ilett]
        ylett = yoff[ilett]
        ax.plot([xlett, xlett], [ylett - trunks[ilett], ylett], 'k')
        mrs = MORSE_CODE_DICT[letter]
        for idit, ditdash in enumerate(mrs):
            if ditdash == '.':
                xwid = dashlength * pct
            else:
                xwid = dashlength
            endpts.append([xlett - xwid / 2., ylett, xwid])
            c_arr.append(clrs[ilett])
            ylett -= yspacing
    endpts = np.array(endpts)

    for iseg, segs in enumerate(endpts):
        ax.add_patch(Rectangle((segs[0], segs[1]), segs[2], linewidth, color=c_arr[iseg], alpha=.5, edgecolor=None))

    plt.xlim((-dashlength / 2., xspacing[-1] + dashlength / 2.))
    plt.ylim((min([min(yoff - trunks), min(endpts[:, 1]) - linewidth]), max(endpts[:, 1] + linewidth)))
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # horizontal('FERAL')
    vertical('FERAL')
