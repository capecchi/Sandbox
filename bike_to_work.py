import matplotlib.pyplot as plt
import numpy as np

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

if __name__ == '__main__':
	pass
