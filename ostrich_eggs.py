'''
PUZZLE: Oskar and the Ostrich Eggs

In preparation for an ad campaign, the Flightless Ostrich Farm needs to test its eggs for durability.  The world standard for egg-hardness calls for rating an egg according to the the highest floor of the Empire State Building from which the egg can be dropped without breaking.

Flightless's official tester, Oskar, realizes that if he takes only one egg along on his trip to New York, he'll need to drop it from (potentially) every one of the building's 102 floors, starting with the first, to determine its rating.

How many drops does he need in the worst case, if he takes two eggs?
'''

import numpy as np
import matplotlib.pyplot as plt

ndrops = np.arange(0, 16)
drop_sequence = []
floor_seq = []
for nd in ndrops:
    drop_sequence.append(''.join(['1'.zfill(n) for n in np.arange(nd, 1, -1)]))
    floor_seq.append(','.join([str(s) for s in np.cumsum(np.arange(nd, 1, -1))]))
max_floor = [len(ds) for ds in drop_sequence]
theor_max = [np.sum(np.arange(n, 1, -1)) for n in ndrops]

isol = np.where(np.array(max_floor) >= 102)[0][0]
print(f'\ndrop_sequence: {drop_sequence[isol]}')
print(f'floor_sequence: {floor_seq[isol]}\n')
plt.step(ndrops, max_floor, 'o-', where='mid')
plt.axvline(ndrops[isol], color='k', linestyle='--', alpha=0.5)
plt.xlabel('ndrops')
plt.ylabel('max_floor')
plt.show()
