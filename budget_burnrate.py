import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']

planned1 = [0, 321537.30, 328790.89, 334463.70]
planned2 = [0, 56001, 94000, 79999]
cumsum_planned1 = np.cumsum(planned1)
cumsum_planned2 = np.cumsum(planned2)
planned1_yrend = [datetime.date(2018, 3, 1) + relativedelta(years=y) for y in range(len(planned1))]
planned2_yrend = [datetime.date(2022, 6, 1) + relativedelta(years=y) for y in range(len(planned2))]

budget = 1530838.
enddate = datetime.date(2025, 5, 31)
monthly_total = [0, 0, 0, 0, 9084.90, 11517.08, 11807.85, 5982.30, 5138.27, 3110.05, 8042.70, 6349.43, 4740.26, 3234.54,
                 4873.06, 16235.86, 9876.40, 17631.64, 19381.48, 24456.76, 23495.18, 24328.68, 22605.01, 22883.81,
                 22604.98, 23766.24, 22604.98, 21243.40, 37853.33, 21206.06, 22528.13, 19634.29, 20791.36, 20402.78,
                 20683.58, 20666.49, 20788.86, 20459.42, 20186.81, 40816.52, 6896.52, 11608.64, 13744.73, 16485.58,
                 26248.47, 16485.62, 16039.65, 18545.30, 17351.91, 19040.35, 25266.45, 16844.30, 17410.97, 17410.96,
                 19037.33, 19887.69, 34021.18, 20306.56, 20073.17, 20715.24, 21918.55, 20841.00, 30864.77, 22107.83,
                 21143.31, 31261.88, 23145.66, 30244.81, 22870.15, 22968.23, 31060.01, 21009.94, 20734.36, 30751.19,
                 20471.23, 23651.91]
cumsum = np.cumsum(monthly_total)
period = [datetime.date(2018, 7, 1) + relativedelta(months=m) for m in range(len(monthly_total))]

# fit burn rate
ignore_months = 18  # ignore first years spendrate
fit = np.polyfit(
    [(period[ignore_months:][i] - period[ignore_months:][0]).days for i in range(len(period[ignore_months:]))],
    cumsum[ignore_months:], 1)
pred_final = fit[0] * (enddate - period[-1]).days + cumsum[-1]
# fit recent burn rate
fit2 = np.polyfit(
    [(period[-12:][i] - period[-12:][0]).days for i in range(len(period[-12:]))], cumsum[-12:], 1)
pred_final2 = fit2[0] * (enddate - period[-1]).days + cumsum[-1]
planned_rate1 = cumsum_planned1[-1] / ((planned1_yrend[-1] - planned1_yrend[0]).days * 12 / 365)
planned_rate2 = cumsum_planned2[-1] / ((planned2_yrend[-1] - planned2_yrend[0]).days * 12 / 365)

igap2 = np.where(np.array(period) == planned2_yrend[0])[0][0]
igap1 = np.where(np.array(period) == planned1_yrend[-1])[0][0]
gap_spending = cumsum[igap2] - cumsum[igap1]

fs = 16
fs2 = 11
fig, ax = plt.subplots(figsize=(8, 5))
ax.axhline(budget * 1.e-6, c='r', ls='--')
ax.axvline(enddate, c='k', ls='--')
ax.annotate('budget', (datetime.date(2019, 1, 1), budget * 1.e-6 + .05), fontsize=fs2, color='r', fontweight='bold')
ax.annotate('end\ndate', (enddate - datetime.timedelta(weeks=25), 1.7), rotation=90, fontsize=fs2, fontweight='bold')

# projections
# ax.plot([period[-1], enddate], np.array([cumsum[-1], pred_final])*1.e-6, '--',
#          label=f'avg burn rate: ${fit[0] * 365 / 12 / 1000.:.1f}k/mo\noverrun: ${pred_final - budget:.0f}', c=clrs[1])
# ax.plot([period[-1], enddate], np.array([cumsum[-1], pred_final2])*1.e-6, '--',
#          label=f'past yr burn rate: ${fit2[0] * 365 / 12 / 1000.:.1f}k/mo\noverrun: ${pred_final2 - budget:.0f}',
#          c=clrs[2])

ax.plot(period, cumsum * 1.e-6, c=clrs[0])

ax.plot(planned1_yrend, cumsum_planned1 * 1.e-6, 'gd--',
        label=f'planned original budget\n${planned_rate1 / 1000.:.1f}k/mo')
ax.plot(planned2_yrend, (cumsum_planned2 + cumsum_planned1[-1] + gap_spending) * 1.e-6, 'gd-',
        label=f'planned first extension\n${planned_rate2 / 1000.:.1f}k/mo')
ax.plot(period[igap1:igap2], (cumsum[igap1:igap2] + cumsum_planned1[-1] - cumsum[igap1]) * 1.e-6, 'g:', alpha=0.5,
        label='gap spending')
ax.plot(period, cumsum * 1.e-6, label=f'spending\n(past yr: ${fit2[0] * 365 / 12 / 1000.:.1f}k/mo)', c=clrs[0])
ax.plot(period[-1], cumsum[-1] * 1.e-6, 'ko')

# proposed budget 289k
prop_enddate = datetime.date(2026, 6, 1)
prop_budget = 289000.
prop_rate = prop_budget / ((prop_enddate - enddate).days * 12 / 365)

ax.plot([enddate, prop_enddate], [budget * 1.e-6, (budget + prop_budget) * 1.e-6], 'o-', c=clrs[1],
        label=f'proposed extension\n${prop_rate / 1000.:.1f}k/mo', linewidth=2)

ax.set_ylabel('spending (M$)', fontsize=fs)
ax.set_xlabel('year', fontsize=fs)
ax.tick_params(labelsize=fs - 2)

plt.legend(framealpha=1, fontsize=fs2, loc='lower right')
plt.tight_layout()
plt.show()

if __name__ == '__main__':
    pass
