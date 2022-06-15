import matplotlib.pyplot as plt
import numpy as np

def color_cycle_demo():
	prop_cycle = plt.rcParams['axes.prop_cycle']
	colors = prop_cycle.by_key()['color']
	
x = np.linspace(0, 10)
p = plt.plot(x, x ** 2, x, x ** 3)
plt.plot(x, 2 * x ** 2, c=p[0].get_color(), ls='--')
plt.plot(x, 0.8 * x ** 3, c=p[-1].get_color(), ls='--')
plt.show()
