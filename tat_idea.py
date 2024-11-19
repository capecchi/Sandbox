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

pct = 1 / 3.  # fraction a dot occupies
dashlength = 1
linespacing = 1
linewidth = .2 * linespacing

word = 'FERAL'


def horizontal():
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


def vertical():
    mtn = np.array([[0, 0], [1, 3], [1.5, 2], [2.3, 2.5], [3, .3]])
    plt.plot(mtn[:, 0], mtn[:, 1])
    plt.show()


if __name__ == '__main__':
    # horizontal()
    vertical()
