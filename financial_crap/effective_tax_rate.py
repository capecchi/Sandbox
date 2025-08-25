import numpy as np
import matplotlib.pyplot as plt
import matplotlib

"""
Just want to visualize what the effective tax rate is for various incomes
Based on 2024 IRS data
"""

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

income = np.linspace(1, 125, num=1000)
rates = [.1, .12, .22, .24, .32, .35, .37]
caps = [11.600, 47.150, 100.525, 191.950, 243.725, 609.350, np.inf]  # in k$
itrunc = min(np.where(caps > max(income))[0]) + 1
rates, caps = rates[:itrunc], caps[:itrunc]
pcts = [r * 100. for r in rates]

floors = caps[:-1]
floors.insert(0, 0)
diff = [caps[i] - caps[i - 1] if i != 0 else caps[i] for i in np.arange(len(caps))]
maxtax = [a * b for a, b in zip(diff, rates)]
carrytax = maxtax[:-1]
carrytax.insert(0, 0)

eff = np.zeros_like(income)
for i, inc in enumerate(income):
    itax = min(np.where(caps > inc)[0])  # index of max tax rate
    tax = rates[itax] * (inc - floors[itax]) + np.sum(carrytax[:itax + 1])
    eff[i] = tax / inc * 100.

# for rate in rates:
#     plt.axhline(rate * 100., color='k', linestyle='--')
dcap, dpct = 5, 2
for (pct, cap) in zip(pcts, caps):
    plt.plot([cap, cap], [pct - dpct, pct + dpct], 'k--', alpha=.5)
    plt.plot([cap - dcap, cap + dcap], [pct, pct], 'k--', alpha=.5)

myinc = 95
mytax = np.interp(myinc, income, eff)
myactual = (881.4 / 3670.5) * 100
mydiff = (myactual - mytax) / 100. * 3670.5
print(
    f'at ${myinc}k, the effective tax rate is {mytax:.0f}%, paystubs indicate a tax rate of {myactual:.0f}%, equating to a difference of {mydiff:.2f}$ per paycheck')
plt.plot(income, eff, '-')
plt.xlabel('income (k$)')
plt.ylabel('effective tax rate (%)')
plt.xlim((0, max(income)))

plt.plot(myinc, myactual, 'rx')
plt.plot(myinc, mytax, 'gx')
plt.show()

if __name__ == '__main__':
    pass
