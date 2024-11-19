import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import datetime
import matplotlib.dates as mdates

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

direc = 'C:/Users/willi/PycharmProjects/Sandbox/data/'
fn = f'{direc}100M_registrations.xlsx'
df = pd.read_excel(fn, engine='openpyxl')
jan1 = datetime.datetime(2025, 1, 1)
yr = datetime.timedelta(days=365)
j = 0
for i in df.index:
    rd, lo, lc, ld = df['Race Date'][i], df['Registration Opens'][i], df['Registration Closes'][i], \
        df['Lottery Drawing'][i]
    while rd < jan1:  # bring into this year
        rd, lo, lc, ld = rd + yr, lo + yr, lc + yr, ld + yr
    if all([d is not pd.NaT for d in [rd, lo, lc, ld]]):
        plt.plot(rd, j, 'd', c=clrs[j % 10])
        plt.annotate(df['Race'][i], (rd, j))
        plt.plot([lo, lc], [j, j], f'v--', c=clrs[j % 10])
        plt.plot(ld, j, '^', c=clrs[j % 10])
        j += 1
    else:
        plt.plot(rd, -1, 'ks', alpha=.5)

plt.plot(np.nan, 'kd', label='Race Date')
plt.plot(np.nan, 'kv', label='Lottery Registration Window')
plt.plot(np.nan, 'k^', label='Lottery Drawing')
plt.plot(np.nan, 'ks', alpha=.5, label='Non-lottery 100s')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.gca().yaxis.set_ticks([])
plt.gcf().autofmt_xdate()

plt.show()

if __name__ == '__main__':
    pass
