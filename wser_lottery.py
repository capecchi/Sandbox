"""
Monte Carlo model to predict odds of gaining entry based on current registration data
"""
import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from random import randrange

matplotlib.use('TkAgg')  # allows plotting in debug mode
clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']


def run_lottery(tick_arr, ent_arr):
    nrunrs = 369  # num runners in 1984
    nticks = ent_arr * tick_arr
    # create runner id array
    id_arr, tc_arr, tc_shrt, idnum = [], [], [], 0

    # for testing-----------------
    # ent_arr = [4, 3, 2, 1]
    # tick_arr = [1, 2, 3, 4]
    # nrunrs = 5  #---------------

    for i in np.arange(len(tick_arr)):
        for j in np.arange(tick_arr[i]):
            id_arr.extend(np.arange(idnum, idnum + ent_arr[i]))
            tc_arr.extend(np.ones(ent_arr[i]) * tick_arr[i])
        tc_shrt.extend(np.ones(ent_arr[i], dtype=int) * tick_arr[i])
        idnum = id_arr[-1] + 1
    ids, tcs = [i for i in np.sort(id_arr)], [int(t) for t in tc_arr]
    id_shrt = np.arange(np.sum(ent_arr))

    # pick runners
    ids_chosen = []
    while len(ids_chosen) < nrunrs:
        id_picked = ids[randrange(len(ids))]
        if id_picked not in ids_chosen:
            ids_chosen.extend([id_picked])

    # compute results
    tick_picks = np.array([tc_shrt[i] for i in ids_chosen])  # ticket numbers of those chosen
    pcts = []
    for i in np.arange(len(tick_arr)):
        num_picked = len(np.where(np.array(tick_picks) == tick_arr[i])[0])
        pcts.extend([num_picked / ent_arr[i]])
    return np.array(pcts)


def get_current_distribution():
    num_tickets = [2 ** n for n in np.arange(10)]
    entrants = [4037, 2474, 1476, 865, 435, 318, 200, 83, 20, 1]
    return np.array(num_tickets), np.array(entrants)


def run_nsims(nruns, showevery=10, ihave=1):
    t1 = datetime.datetime.now()
    nt, en = get_current_distribution()
    w, pcts_agg = None, None
    fig, ax = plt.subplots()
    for irun in np.arange(nruns) + 1:
        pcts = run_lottery(nt, en)
        if w is None:
            w = 1
            pcts_agg = pcts
        else:
            pcts_agg = (pcts_agg * w + pcts) / (w + 1)
            w += 1
        if irun % showevery == 0:
            ax.plot(pcts_agg, label=f'run #{irun}')
    ax.set_xticks(np.arange(len(nt)), labels=[f'{t}' for t in nt])
    ax.set_ylabel('pct chosen per ticket count')
    ax.set_xlabel('ticket count')
    plt.legend()
    t2 = datetime.datetime.now()
    print(f'with {ihave} tickets you have a {pcts_agg[np.where(nt == 4)[0][0]] * 100:.1f}% chance of entry')
    print(f'simulation took: {(t2 - t1).seconds} sec')


def run_thresh_sim(pct_thresh=.1, showevery=10, ihave=1):
    t1 = datetime.datetime.now()
    nt, en = get_current_distribution()
    w, pcts_agg, pct_change = None, None, pct_thresh * 2.  # set above pct thresh to ensure we run at least once
    fig, ax = plt.subplots()
    irun = 0

    while pct_change > pct_thresh:
        pcts = run_lottery(nt, en)
        if w is None:
            w = 1
            pcts_agg = pcts
        else:
            pcts_agg_new = (pcts_agg * w + pcts) / (w + 1)
            pct_change = max(abs(pcts_agg_new - pcts_agg)) * 100.
            pcts_agg = pcts_agg_new
            w += 1
        irun += 1
        if irun % showevery == 0:
            ax.plot(pcts_agg * 100, '--', alpha=0.5, label=f'run #{irun}')
    ax.plot(pcts_agg*100, 'k-', label='final outcome')
    ax.set_xticks(np.arange(len(nt)), labels=[f'{t}' for t in nt])
    ax.set_ylabel('pct chosen per ticket count')
    ax.set_xlabel('ticket count')
    ime = np.where(nt == ihave)[0][0]
    ax.annotate('me', xy=(np.arange(len(nt))[ime], pcts_agg[ime] * 100),
                xytext=(np.arange(len(nt))[ime], pcts_agg[ime] * 100 + 10), arrowprops=dict(facecolor='black'))
    plt.legend()
    t2 = datetime.datetime.now()
    print(f'with {ihave} tickets you have a {pcts_agg[ime] * 100:.2f}% chance of entry')
    print(f'simulation took: {(t2 - t1).seconds} sec and {irun + 1} runs')


if __name__ == '__main__':
    # nt, en = get_current_distribution()
    # run_lottery(nt, en)
    # run_nsims(1000, showevery=20, ihave=2)
    run_thresh_sim(pct_thresh=.01, showevery=50, ihave=2)
    plt.show()
