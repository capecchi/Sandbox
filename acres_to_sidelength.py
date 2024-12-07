import matplotlib.pyplot as plt
import numpy as np

acres = np.linspace(0, 400, num=500, endpoint=True)
conv = 43560.  # sqft/acre
sqft = conv * acres
square_lot_side_ft = np.sqrt(sqft)
sls_mi = square_lot_side_ft / 5280.

fig, ax = plt.subplots()
axr = ax.twinx()
ax.plot(acres, sls_mi)
ax.set_xlabel('acres')
ax.set_title('square plot side length')
ax.set_ylabel('[mi]')
axr.plot(acres, square_lot_side_ft)
axr.set_ylabel('[ft]')
ax.grid(True)
plt.show()
