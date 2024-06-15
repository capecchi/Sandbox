import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import datetime

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']


class Source:
    def __init__(self, name, date, amount, periodicity_days):
        self.name = name
        self.date = date
        self.amount = amount
        self.periodicity = periodicity_days


sources = [Source('UW', datetime.date(2024, 5, 2), 1980.98, 14),
           Source('rent', datetime.date(2024, 5, 1), -1865, 30),
           Source('coaching', datetime.date(2024, 1, 8), -150, 28),
           Source('Netflix', datetime.date(2024, 5, 8), -15.49, 30),
           Source('Audible', datetime.date(2024, 5, 30), -15, 30),
           Source('Spectrum', datetime.date(2024, 5, 14), -58.64, 30),
           Source('Food', datetime.date(2024, 5, 12), -150, 7),
           Source('Car insurance', datetime.date(2024, 5, 10), -68.16, 30),
           Source('Term life', datetime.date(2024, 5, 1), -764.16, 365)]
# mge
# pets
# paycheck increases once dumbshit is off my insurance
# gas

ndays = 365
xdays = [datetime.date(2024, 5, 8) + datetime.timedelta(days=i) for i in range(ndays)]
net = 4552  # amount in checking on 5/8
fig, ax = plt.subplots()
for i in range(ndays):
    for c, src in enumerate(sources):
        if (xdays[i] - src.date).days % src.periodicity == 0:
            ax.plot([xdays[i], xdays[i]], [net, net + src.amount], c=clrs[c], linewidth=2)
            net += src.amount
    if i < ndays - 1:
        ax.plot([xdays[i], xdays[i + 1]], [net, net], 'k')

for i in range(len(sources)):
    ax.plot(np.nan, np.nan, label=sources[i].name, c=clrs[i])
plt.xticks(rotation='vertical')
plt.legend()
plt.show()

if __name__ == '__main__':
    pass
