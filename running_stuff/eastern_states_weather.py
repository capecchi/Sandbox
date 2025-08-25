import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

finish_pct = [50, 37, 34, 52, 59, 51, 60, 58]
yrs = [2014, 2015, 2016, 2017, 2019, 2021, 2022, 2023]
strt_temp = [56, 59, 74, 65, 58, 71, 53, 62]
sat_high = [82, 82, 93, 80, 81, 81, 84, 84]
sun_low = [56, 65, 73, 68, 55, 59, 54, 65]
sun_high = [85, 85, 91, 81, 79, 79, 84, 84]
x = np.array([min(finish_pct), max(finish_pct)])

for i, (set, lbl) in enumerate(zip([strt_temp, sat_high, sun_low, sun_high], ['start temp', 'sat high', 'sun low', 'sun high'])):
    fit = np.polyfit(finish_pct, set, 1)  # [slope, offset]
    plt.plot(finish_pct, set, 'o', c=clrs[i], label=lbl)
    plt.plot(x, x*fit[0]+fit[1], '--', c=clrs[i])
    print(f'{fit[0]} deg/% for {lbl}: 100% at {100*fit[0]+fit[1]}')


# for i, (set, lbl) in enumerate(zip([sat_high, sun_high], ['sat high', 'sun high'])):
#     fit = np.polyfit(finish_pct, set, 1)  # [slope, offset]
#     plt.plot(finish_pct, set, 'o', c=clrs[i], label=lbl)
#     plt.plot(x, x*fit[0]+fit[1], '--', c=clrs[i])
#     print(f'{fit[0]} deg/% for {lbl}')

plt.legend()
plt.xlabel('finish %')
plt.ylabel('temp $\degree$F')
plt.show()

if __name__ == '__main__':
    pass
