#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import datetime

from common import *
from scrape import entorb
from repro import polynomial_r

FUTURE_RANGE = 5 * 365


def plot_projections(names, des, populations, col='Cases', future_range=FUTURE_RANGE, LOG=False):
    """
    Plot graphs of four rates.
    """
    fig, axes = plt.subplots(nrows=int(len(des)/4), ncols=4, sharex=True, sharey=True, figsize=(16,16))
    for name, de, population, ax in zip(names, des, populations, axes.flat):
        de = de.drop(columns=[c for c in de.columns if c != col]).rolling('7D').mean()

        now = de.reset_index()['Date'].tail(1).values[0]

        date_range = pd.date_range(start=now, \
                periods=FUTURE_RANGE/1, \
                freq="%dD" % 1)

        done = set()

        for factor, interval in [(1, 1), (3, 1)]:
            df = de * factor
            rs = polynomial_r(df, population=population, generation_time=1)
            
            r = rs[col].values[-1]

            n = list()
            for i, _ in enumerate(date_range):
                if i == 0:
                    n.append(df[col].tail(1).values[0])
                    continue
                n.append(r * n[-1] * (1. - n[-1]/population))

            proj_col = "Projected %s%s (last %dD avg rate)" % (col, '' if factor==1 else (' x' + str(factor) + ', '), interval)
            proj = pd.DataFrame({ 'Date': date_range, proj_col: n }) \
                    .set_index('Date')

            for d,c in [(df, col), (proj, proj_col)]:
                if (c, factor) in done:
                    continue
                #d[c].plot(ax=ax, logy=LOG, label=(("%s x%d" % (c, factor)) if (c==col and factor!=1) else c))
                d[c].diff(1).plot(ax=ax, logy=LOG, label=("%s x%d" % (c, factor)) if (c==col and factor!=1) else c, title=name)
                done.add((c, factor))

            ax.grid()
            ax.set_ylabel("Daily")
            # ax.legend(handles=axes[1].lines, loc='best')

    fig.suptitle(("COVID-19 spread projection using Logistic map\n"
        "assuming a carrying capacity of K people and dt=%dD tick time.\n"
        "created: %s"
        " author: @pschwede,"
        " source: JHU CSSE via @entorb & @pomber.") \
                % (DAYS_INFECTION_TILL_SYMPTOM, str(now)[:10]))

    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.autofmt_xdate()
    return fig


def plot_projection(de, population, col='Cases', future_range=FUTURE_RANGE, LOG=False):
    """
    Plot graphs of four rates.
    """
    de = de.drop(columns=[c for c in de.columns if c != col]).rolling('7D').mean()

    now = de.reset_index()['Date'].tail(1).values[0]

    date_range = pd.date_range(start=now, \
            periods=FUTURE_RANGE/1, \
            freq="%dD" % 1)

    done = set()

    fig, axes = plt.subplots(nrows=2, sharex=True, figsize=(10,9))
    for factor, interval in [(1, 1), (1, 7), (3, 7), (4, 7)]:
        df = de * factor
        rs = polynomial_r(df, population=population, generation_time=1)
        
        r = rs[col].values[-1]

        n = list()
        for i, _ in enumerate(date_range):
            if i == 0:
                n.append(df[col].tail(1).values[0])
                continue
            n.append(r * n[-1] * (1. - n[-1]/population))

        proj_col = "Projected %s%s (last %dD avg rate)" % (col, '' if factor==1 else (' x' + str(factor) + ', '), interval)
        proj = pd.DataFrame({ 'Date': date_range, proj_col: n }) \
                .set_index('Date')

        for d,c in [(df, col), (proj, proj_col)]:
            if (c, factor) in done:
                continue
            d[c].plot(ax=axes[0], logy=LOG, label=(("%s x%d" % (c, factor)) if (c==col and factor!=1) else c))
            d[c].diff(1).plot(ax=axes[1], logy=LOG, label=("%s x%d" % (c, factor)) if (c==col and factor!=1) else c)
            done.add((c, factor))

    axes[0].grid()
    axes[0].set_ylabel("Total")
    axes[1].grid()
    axes[1].set_ylabel("Daily")
    axes[1].legend(handles=axes[1].lines, loc='best')

    fig.suptitle(("COVID-19 spread projection using Logistic map\n"
        "assuming a carrying capacity of K=%dM people and dt=%dD tick time.\n"
        "created: %s"
        " author: @pschwede,"
        " source: JHU CSSE via @entorb & @pomber.") \
                % (population/1e6, DAYS_INFECTION_TILL_SYMPTOM, str(now)[:10]))

    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.autofmt_xdate()
    return fig


def plot_future_unld(de, population, col='Cases', future_range=FUTURE_RANGE, LOG=False):
    """
    """
    fig, axes = plt.subplots(nrows=2, sharex=True, figsize=(10,9))

    FACTOR = 3
    
    df = de * FACTOR
    rs = polynomial_r(df, population=population, generation_time=1)
    
    contemp_r = rs[col].values[-1]
    r = contemp_r

    now = de.reset_index()['Date'].tail(1).values[0]
    date_range = pd.date_range(start=now, \
            periods=FUTURE_RANGE/1, \
            freq="%dD" % 1)

    n = list()
    for i, _ in enumerate(date_range):
        if i == 0:
            n.append(df[col].tail(1).values[0])
            continue
        # apply gov rules at turning point when weekly infections per 100000 sink below 100
        if i > 8 and 50 <= 1e5*(n[-7]-n[-1])/population <= 100:
            r = 1.6
        else:
            r = contemp_r
        n.append(max(n[-1], r * n[-1] * (1. - n[-1]/population)))

    proj_col = "Projected %s x%d (last 1D avg rate)" % (col, FACTOR)
    proj = pd.DataFrame({ 'Date': date_range, proj_col: n }) \
            .set_index('Date')

    for d, c in [(df, col), (proj, proj_col)]:
        d[c].plot(ax=axes[0], logy=LOG, label="%s x%d" % (c, FACTOR))
        d[c].diff(1).plot(ax=axes[1], logy=LOG, label="%s x%d" % (c, FACTOR))

    axes[0].grid()
    axes[0].set_ylabel("Total")
    axes[1].grid()
    axes[1].set_ylabel("Daily")
    axes[1].legend(handles=axes[1].lines, loc='best')

    fig.suptitle(("COVID-19 spread projection using Logistic map\n"
        "assuming a carrying capacity of K=%dM people and dt=%dD tick time.\n"
        "created: %s"
        " author: @pschwede,"
        " source: JHU CSSE via @entorb & @pomber.") \
                % (population/1e6, DAYS_INFECTION_TILL_SYMPTOM, str(now)[:10]))

    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.autofmt_xdate()
    return fig


def main():
    import sys
    if len(sys.argv) < 3:
        print("USAGE: %s OUTFILEprojection1 OUTFILEfuture_unld2" % sys.argv[0])
        sys.exit(2)
    de = entorb.to_dataframe('DE-total')
    with plt.style.context('ggplot'):
        plot_projection(de, DE_POPULATION).savefig(sys.argv[1], bbox_inches='tight')
        DE_STATE_NAMES,
        plot_projections([entorb.to_dataframe(s) for s in DE_STATE_NAMES], \
                [DE_STATE_POPULATION[DE_STATE_NAMES[s]] for s in DE_STATE_NAMES]) \
                .savefig(sys.argv[2], bbox_inches='tight')
        plot_projection(de=entorb.to_dataframe(nation='US'), population=329e6).savefig(sys.argv[3], bbox_inches='tight')


if __name__ == "__main__":
    main()

