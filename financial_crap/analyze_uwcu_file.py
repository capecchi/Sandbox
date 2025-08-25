import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import datetime

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

direc = 'C:/Users/willi/PycharmProjects/Sandbox/financial_crap/data/'
fp = f'{direc}History.csv'
fp2 = f'{direc}Chase4159_Activity20230607_20250607_20250607.csv'
df = pd.read_csv(fp)
bal = [float(b.replace('$', '')) for b in df['Balance']]
dat = [datetime.datetime.strptime(d, '%m/%d/%Y') for d in df['Posted Date']]
udat, iu = np.unique(dat, return_index=True)
ubal = np.array(bal)[iu]
udelt = [(d - udat[0]).days for d in udat]

interpdat = [ts.to_pydatetime() for ts in
             pd.date_range('2024-05-01', datetime.datetime.today().strftime('%Y-%m-%d'), freq='MS')]
interpdelt = [(d - udat[0]).days for d in interpdat]
interpbal = np.interp(interpdelt, udelt, ubal)

df2 = pd.read_csv(fp2)
idat = [ts.to_pydatetime() for ts in
        pd.date_range('2024-06-01', datetime.datetime.today().strftime('%Y-%m-%d'), freq='MS')]
cats = np.array([str(v) for v in df2['Category'].values])
ucats = np.unique([c for c in cats if c != 'nan'])
dc = np.array([datetime.datetime.strptime(d, '%m/%d/%Y') for d in df2['Transaction Date']])
amts = np.array(
    [-float(d) for d in df2['Amount'].values])  # negative here so spent amounts are positive, refunds negative
# dfp = {'month': idat[:-1]}
months = [d.strftime("%b '%y") for d in idat[:-1]]
dfp = pd.DataFrame({}, index=months)
tot = np.zeros(len(idat[:-1]))

for cat in ucats:
    dfp[f'{cat}'] = np.zeros(len(idat[:-1]))
for im in np.arange(len(idat[:-1])):
    iok = np.where((dc >= idat[im]) & (dc < idat[im + 1]) & (amts > 0))
    tot[im] = np.sum(amts[iok])
    for cat in ucats:
        iok = np.where((dc >= idat[im]) & (dc < idat[im + 1]) & (cats == cat))
        dfp[f'{cat}'][im] = np.sum(amts[iok])

plt.figure()
plt.plot(dat, bal, 'bo-')
plt.plot(udat, ubal, 'rd--')
plt.plot(interpdat, interpbal, 'gs:')

ax = dfp.plot.bar(rot=45, stacked=True)
# axr = ax.twinx()
# axr.plot(months, tot, 'o-')
plt.show()
a = 1

if __name__ == '__main__':
    pass
