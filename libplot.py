
from libcommon import *

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

font = {"size": 14}
matplotlib.rc("font", **font)

def plot_by_date(state, data, xticks=[], xticklabels=[], xylim_s=[], multiple=None, norm=False):
    if xticks == []:
        days = data['date']
        ddays = time_delta(data['date'])
        for d,dd in zip(days, ddays):
            if d.day == 1:
                xticks.append(dd)
                xticklabels.append(d.strftime("%Y-%m-%d"))
    #
    fig, ax = plt.subplots(2, 2, figsize=(16, 10), sharex=True)
    #
    if xylim_s == []:
        xylim_s = np.zeros((2, 2, 2, 2), dtype=float)   # j, i, x/y, range
    for j,Y in enumerate(['', '.incr']):
        for i,(X,color) in enumerate(zip(['cases', 'deaths'], ['red', 'black'])):
            key = '%s%s'%(X,Y)
            #
            if multiple is not None:
                cs = plt.cm.get_cmap("Spectral")(np.linspace(0, 1, len(multiple)))
                for c,m in zip(cs, multiple):
                    if m is None: continue
                    n = m[key]
                    if norm:
                        n = n.astype(float) / m['norm']
                    #ax[j,i].plot(time_delta(m['date']), n, 'x', linewidth=0.5, ms=2, color=c)
                    ax[j,i].plot(time_delta(m['date']), smooth(m['date'], n), '-', linewidth=1, color=c)
            #
            n = data[key]
            if norm:
                n = n.astype(float) / data['norm']
            #
            ax[j,i].plot(time_delta(data['date']), n, 'x', linewidth=1, ms=5, color=color)
            ax[j,i].plot(time_delta(data['date']), smooth(data['date'], n), '-', linewidth=2.5, color=color)
            #
            ax[j,i].grid(True, linewidth=0.5)
            if j == 0:
                ax[j,i].set_yscale("log")
            ax[j,i].set_xticks(xticks)
            ax[j,i].set_xticklabels(xticklabels, rotation=15)
            #
            xlim = xylim_s[j,i,0]
            if xlim[1]-xlim[0] > 0.0:
                ax[j,i].set_xlim(xlim)
            else:
                xylim_s[j,i,0] = ax[j,i].get_xlim()
            ylim = xylim_s[j,i,1]
            if ylim[1]-ylim[0] > 0.0 and j == 0:
                ax[j,i].set_ylim(ylim)
            else:
                if j == 0:
                    ax[j,i].set_ylim(bottom=10**(1-i))
                else:
                    ax[j,i].set_ylim(bottom=0)
                xylim_s[j,i,1] = ax[j,i].get_ylim()
    #
    fig.tight_layout()
    if norm:
        plt.savefig("%s/by_date.norm/%s.png"%(OUTPUT, state))
    else:
        plt.savefig("%s/by_date/%s.png"%(OUTPUT, state))
    plt.close("all")
    #
    pltargs = {"xylim_s": xylim_s, "xticks": xticks, "xticklabels": xticklabels}
    return pltargs

def plot_by_case(state, data, xylim_s=[], multiple=None, norm=False):
    fig, ax = plt.subplots(2, 2, figsize=(16, 10))
    if xylim_s == []:
        xylim_s = np.zeros((2, 2, 2, 2), dtype=float)   # j, i, x/y, range
    color='red'
    for j,Y in enumerate(['cases.incr', 'deaths.incr']):
        for i,X in enumerate(['cases', 'deaths']):
            if multiple is not None:
                cs = plt.cm.get_cmap("Spectral")(np.linspace(0, 1, len(multiple)))
                for c,m in zip(cs, multiple):
                    if m is None: continue
                    x = m[X] ; y = m[Y]
                    if norm:
                        x = x.astype(float) / m['norm']
                        y = y.astype(float) / m['norm']
                    x = smooth(m['date'], x)
                    y = smooth(m['date'], y)
                    ax[j,i].plot(x, y, '-', linewidth=1, color=c)

            x = data[X] ; y = data[Y]
            if norm:
                x = x.astype(float) / data['norm']
                y = y.astype(float) / data['norm']
            x = smooth(data['date'], data[X])
            y = smooth(data['date'], data[Y])
            ax[j,i].plot(x, y, '-', linewidth=2.5, color=color)
            #
            ax[j,i].grid(True, linewidth=0.5)
            ax[j,i].set_xscale("log")
            ax[j,i].set_yscale("log")
            #
            xlim = xylim_s[j,i,0]
            if xlim[1]-xlim[0] > 0.0:
                ax[j,i].set_xlim(xlim)
            else:
                ax[j,i].set_xlim(left=10**(-i))
                xylim_s[j,i,0] = ax[j,i].get_xlim()
            ylim = xylim_s[j,i,1]
            if ylim[1]-ylim[0] > 0.0:
                ax[j,i].set_ylim(ylim)
            else:
                ax[j,i].set_ylim(bottom=10**(-j))
                xylim_s[j,i,1] = ax[j,i].get_ylim()
    #
    fig.tight_layout()
    if norm:
        plt.savefig("%s/by_case.norm/%s.png"%(OUTPUT, state))
    else:
        plt.savefig("%s/by_case/%s.png"%(OUTPUT, state))
    plt.close("all")
    #
    pltargs = {"xylim_s": xylim_s}
    return pltargs
