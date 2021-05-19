import matplotlib.pyplot as plt
import numpy as np

n0 = 1e19
a = 0.2
nu = [1, 1.1, 1.9, 2,3,4]

x = np.linspace(0, a)
for n in nu:
    y = n0 * (1 - x ** 2 / a ** 2) ** n
    plt.plot(x, y, label=n)
# plt.axvspan(3, 4, alpha=0.5, color='k')
# plt.annotate('nbi on', (3, 8))
plt.legend()
plt.show()
