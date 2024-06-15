import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime as dt

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 5/9/24
# I hate this and I don't want to see her every week
# I need to get out of Madison so I can take the dogs and be done with her

y = 2024
dog_swaps = [dt.date(y, 5, 13),
             dt.date(y, 5, 26),  # before 27th
             dt.date(y, 6, 4),  # after 3rd
             dt.date(y, 6, 15),  # plan to fly out on 16th
             dt.date(y, 6, 24),  # flexible here +/- either way
             dt.date(y, 7, 2),  # flexible here
             dt.date(y, 7, 8),  # flexible
             dt.date(y, 7, 14),  # plan to fly on 15th
             dt.date(y, 7, 27),  # driving back from lake on 27th
             dt.date(y, 8, 7),  # fly out on 8th
             dt.date(y, 8, 18),  # fly to MSP for Capecchi picnic on 17th, back on 18th?
             ]

bd, sd = [], []
bill = 1
for i in range(len(dog_swaps) - 1):
    if bill:
        plt.plot([dog_swaps[i], dog_swaps[i + 1]], [1, 1], linewidth=2, c=clrs[0])
        bd.append((dog_swaps[i + 1] - dog_swaps[i]).days)
    else:
        plt.plot([dog_swaps[i], dog_swaps[i + 1]], [-1,-1], linewidth=2, c=clrs[1])
        sd.append((dog_swaps[i + 1] - dog_swaps[i]).days)
    bill = (bill + 1) % 2

princeton = [(dt.date(y, 5, 27), dt.date(y, 6, 3)), (dt.date(y, 6, 16), dt.date(y, 6, 21)),
             (dt.date(y, 7, 15), dt.date(y, 7, 27)), (dt.date(y, 8, 8), dt.date(y, 8, 18))]
print(f'bill: {sum(bd)} days, {bd}')
print(f'steph: {sum(sd)} days, {sd}')

for p in princeton:
    plt.plot([p[0], p[1]], [0, 0], 'k')

plt.plot(np.nan, np.nan, c=clrs[0], label='Bill')
plt.plot(np.nan, np.nan, c=clrs[1], label='Steph')
plt.plot(np.nan, np.nan, c='k', label='Princeton')
plt.legend()
plt.ylim((-5, 5))
plt.show()

if __name__ == '__main__':
    pass
